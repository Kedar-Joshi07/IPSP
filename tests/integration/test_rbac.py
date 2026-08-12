"""Phase 1F role-to-permission enforcement and provisioning integration tests."""

from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated

import pytest
from alembic import command
from alembic.config import Config
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from ipsp.api.dependencies.auth import require_csrf
from ipsp.api.dependencies.rbac import require_permission
from ipsp.auth.rbac import CORE_PERMISSION_CODES, CorePermission
from ipsp.auth.service import AuthPrincipal
from ipsp.cli.rbac import main as rbac_cli_main
from ipsp.cli.rbac import synchronize_core_rbac
from ipsp.config.settings import Settings
from ipsp.database.models import Permission, Role, RolePermission, User, UserSession
from ipsp.errors.exceptions import IPSPError, PermissionDeniedException
from ipsp.main import create_app
from sqlalchemy import func, select

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PASSWORD = "rbac-test-password-秘密"


@pytest.fixture
def rbac_app(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[FastAPI]:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
    app = create_app(settings)
    try:
        yield app
    finally:
        app.state.foundation_services.database_engine.dispose()


def _role(app: FastAPI, name: str) -> Role:
    services = app.state.foundation_services
    with services.database_sessions.session() as session:
        role = session.scalar(select(Role).where(Role.name == name))
        assert role is not None
        session.expunge(role)
        return role


def _add_role(app: FastAPI, name: str) -> int:
    services = app.state.foundation_services
    with services.database_sessions.transaction() as session:
        role = Role(name=name, description=None)
        session.add(role)
        session.flush()
        return role.id


def _add_user(app: FastAPI, username: str, role_id: int, *, active: bool = True) -> int:
    services = app.state.foundation_services
    now = datetime.now(UTC)
    with services.database_sessions.transaction() as session:
        user = User(
            username=username,
            display_name=username.title(),
            email=None,
            password_hash=services.password_service.hash(PASSWORD),
            role_id=role_id,
            is_active=active,
            must_change_password=False,
            failed_login_count=0,
            locked_until=None,
            last_login_at=None,
            password_changed_at=now,
            created_at=now,
            created_by=None,
            updated_at=now,
        )
        session.add(user)
        session.flush()
        return user.id


def _map_permission(app: FastAPI, role_id: int, code: str) -> None:
    services = app.state.foundation_services
    with services.database_sessions.transaction() as session:
        permission = session.scalar(select(Permission).where(Permission.code == code))
        assert permission is not None
        session.add(RolePermission(role_id=role_id, permission_id=permission.id))


def _login(client: TestClient, username: str):
    return client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": PASSWORD},
    )


def test_core_permission_catalog_is_exact_and_typed() -> None:
    assert {permission.value for permission in CorePermission} == {
        "simulation.run",
        "simulation.export",
        "dataset.view",
        "dataset.upload",
        "dataset.configure",
        "dataset.assign",
        "model.train",
        "model.promote",
        "llm.configure",
        "internet.configure",
        "user.manage",
        "logs.view",
        "system.configure",
    }
    assert frozenset(permission.value for permission in CorePermission) == CORE_PERMISSION_CODES
    assert len(CORE_PERMISSION_CODES) == 13
    assert all("*" not in code for code in CORE_PERMISSION_CODES)


def test_catalog_sync_is_additive_idempotent_and_preserves_custom_data(
    rbac_app: FastAPI,
) -> None:
    services = rbac_app.state.foundation_services
    custom_role_id = _add_role(rbac_app, "CustomRole")
    with services.database_sessions.transaction() as session:
        custom_permission = Permission(code="plugin.example", description="Custom extension")
        session.add(custom_permission)
        session.flush()
        session.add(RolePermission(role_id=custom_role_id, permission_id=custom_permission.id))

    first = services.rbac_catalog_service.ensure_core_catalog()
    second = services.rbac_catalog_service.ensure_core_catalog()

    assert first.roles_created == 2
    assert first.permissions_created == 13
    assert first.admin_mappings_created == 13
    assert first.sessions_invalidated_for_users == 0
    assert first.changed is True
    assert second.roles_created == 0
    assert second.permissions_created == 0
    assert second.admin_mappings_created == 0
    assert second.sessions_invalidated_for_users == 0
    assert second.changed is False
    with services.database_sessions.session() as session:
        permission_codes = set(session.scalars(select(Permission.code)))
        admin = session.scalar(select(Role).where(Role.name == "Admin"))
        user = session.scalar(select(Role).where(Role.name == "User"))
        custom = session.scalar(select(Role).where(Role.name == "CustomRole"))
        assert admin is not None and user is not None and custom is not None
        admin_codes = set(
            session.scalars(
                select(Permission.code)
                .join(RolePermission)
                .where(RolePermission.role_id == admin.id)
            )
        )
        user_codes = set(
            session.scalars(
                select(Permission.code)
                .join(RolePermission)
                .where(RolePermission.role_id == user.id)
            )
        )
        custom_codes = set(
            session.scalars(
                select(Permission.code)
                .join(RolePermission)
                .where(RolePermission.role_id == custom.id)
            )
        )
    assert permission_codes == CORE_PERMISSION_CODES | {"plugin.example"}
    assert admin_codes == CORE_PERMISSION_CODES
    assert user_codes == set()
    assert custom_codes == {"plugin.example"}


def test_authorization_fail_closed_and_has_no_admin_name_bypass(rbac_app: FastAPI) -> None:
    services = rbac_app.state.foundation_services
    services.rbac_catalog_service.ensure_core_catalog()
    admin_id = _add_user(rbac_app, "named-admin", _role(rbac_app, "Admin").id)
    analyst_role_id = _add_role(rbac_app, "Analyst")
    analyst_id = _add_user(rbac_app, "analyst", analyst_role_id)
    inactive_id = _add_user(rbac_app, "inactive", analyst_role_id, active=False)
    _map_permission(rbac_app, analyst_role_id, CorePermission.USER_MANAGE)

    assert services.rbac_service.has_permission(analyst_id, CorePermission.USER_MANAGE) is True
    assert services.rbac_service.has_permission(inactive_id, CorePermission.USER_MANAGE) is False
    assert services.rbac_service.has_permission(999_999, CorePermission.USER_MANAGE) is False
    assert services.rbac_service.has_permission(analyst_id, "unknown.permission") is False
    assert services.rbac_service.has_permission(analyst_id, "*") is False

    admin_role_id = _role(rbac_app, "Admin").id
    assert services.rbac_service.replace_role_permissions(admin_role_id, set()) is True
    assert services.rbac_service.has_permission(admin_id, CorePermission.USER_MANAGE) is False
    with pytest.raises(PermissionDeniedException) as denied:
        services.rbac_service.enforce_permission(admin_id, CorePermission.USER_MANAGE)
    assert denied.value.error_code == "AUTHZ-PERMISSION_DENIED"
    assert denied.value.safe_message == "Permission denied."

    with services.database_sessions.transaction() as session:
        analyst = session.get(Role, analyst_role_id)
        assert analyst is not None
        analyst.name = "RenamedRole"
    assert services.rbac_service.has_permission(analyst_id, CorePermission.USER_MANAGE) is True

    assert services.rbac_service.replace_role_permissions(analyst_role_id, set()) is True
    assert services.rbac_service.has_permission(analyst_id, CorePermission.USER_MANAGE) is False
    with pytest.raises(PermissionDeniedException):
        services.rbac_service.enforce_permission(analyst_id, "unknown.permission")


def test_permission_dependency_and_csrf_composition(rbac_app: FastAPI) -> None:
    services = rbac_app.state.foundation_services
    services.rbac_catalog_service.ensure_core_catalog()
    admin_id = _add_user(rbac_app, "admin-user", _role(rbac_app, "Admin").id)
    user_id = _add_user(rbac_app, "regular-user", _role(rbac_app, "User").id)
    disabled_id = _add_user(
        rbac_app,
        "disabled-user",
        _role(rbac_app, "Admin").id,
        active=False,
    )
    assert len({admin_id, user_id, disabled_id}) == 3
    permission_dependency = require_permission(CorePermission.USER_MANAGE)

    @rbac_app.get("/test-rbac-protected")
    def protected_get(
        principal: Annotated[AuthPrincipal, Depends(permission_dependency)],
    ) -> dict[str, int]:
        return {"user_id": principal.user_id}

    @rbac_app.post("/test-rbac-protected")
    def protected_post(
        principal: Annotated[AuthPrincipal, Depends(permission_dependency)],
        _csrf: Annotated[AuthPrincipal, Depends(require_csrf)],
    ) -> dict[str, int]:
        return {"user_id": principal.user_id}

    with TestClient(rbac_app, base_url="https://testserver") as anonymous:
        unauthenticated = anonymous.get("/test-rbac-protected")
    assert unauthenticated.status_code == 401, unauthenticated.text

    with TestClient(rbac_app, base_url="https://testserver") as disabled:
        disabled_response = _login(disabled, "disabled-user")
    assert disabled_response.status_code == 401

    with TestClient(rbac_app, base_url="https://testserver") as regular:
        assert _login(regular, "regular-user").status_code == 200
        denied = regular.get("/test-rbac-protected")
        csrf = regular.cookies.get(rbac_app.state.settings.auth.csrf_cookie_name)
        assert csrf
        denied_post = regular.post(
            "/test-rbac-protected",
            headers={rbac_app.state.settings.auth.csrf_header_name: csrf},
        )
    for response in (denied, denied_post):
        assert response.status_code == 403
        assert response.json()["error_code"] == "AUTHZ-PERMISSION_DENIED"
        assert response.json()["message"] == "Permission denied."
        assert response.json()["trace_id"]
        assert "Admin" not in response.text
        assert CorePermission.USER_MANAGE not in response.text

    with TestClient(rbac_app, base_url="https://testserver") as admin:
        login = _login(admin, "admin-user")
        assert login.status_code == 200
        allowed = admin.get("/test-rbac-protected")
        missing_csrf = admin.post("/test-rbac-protected")
        csrf = admin.cookies.get(rbac_app.state.settings.auth.csrf_cookie_name)
        assert csrf
        allowed_post = admin.post(
            "/test-rbac-protected",
            headers={rbac_app.state.settings.auth.csrf_header_name: csrf},
        )
    assert allowed.status_code == 200
    assert allowed_post.status_code == 200
    assert missing_csrf.status_code == 403
    assert missing_csrf.json()["error_code"] == "AUTHZ-CSRF_INVALID"

    admin_role_id = _role(rbac_app, "Admin").id
    services.rbac_service.replace_role_permissions(admin_role_id, set())
    with TestClient(rbac_app, base_url="https://testserver") as unmapped_admin:
        assert _login(unmapped_admin, "admin-user").status_code == 200
        admin_name_is_not_authority = unmapped_admin.get("/test-rbac-protected")
    assert admin_name_is_not_authority.status_code == 403
    assert admin_name_is_not_authority.json()["error_code"] == "AUTHZ-PERMISSION_DENIED"

    analyst_role_id = _add_role(rbac_app, "Analyst")
    analyst_id = _add_user(rbac_app, "mapped-analyst", analyst_role_id)
    assert analyst_id not in {admin_id, user_id, disabled_id}
    _map_permission(rbac_app, analyst_role_id, CorePermission.USER_MANAGE)
    with services.database_sessions.transaction() as session:
        analyst_role = session.get(Role, analyst_role_id)
        assert analyst_role is not None
        analyst_role.name = "RenamedAnalyst"
    with TestClient(rbac_app, base_url="https://testserver") as analyst:
        assert _login(analyst, "mapped-analyst").status_code == 200
        mapped_non_admin = analyst.get("/test-rbac-protected")
    assert mapped_non_admin.status_code == 200


def test_user_role_change_invalidates_only_changed_users_sessions(rbac_app: FastAPI) -> None:
    services = rbac_app.state.foundation_services
    services.rbac_catalog_service.ensure_core_catalog()
    user_role = _role(rbac_app, "User")
    analyst_role_id = _add_role(rbac_app, "Analyst")
    alice_id = _add_user(rbac_app, "alice", user_role.id)
    bob_id = _add_user(rbac_app, "bob", user_role.id)
    alice_one = services.auth_service.login("alice", PASSWORD)
    alice_two = services.auth_service.login("alice", PASSWORD)
    bob = services.auth_service.login("bob", PASSWORD)

    assert services.rbac_service.assign_user_role(alice_id, user_role.id) is False
    services.auth_service.authenticate_session(alice_one.session_token)
    assert services.rbac_service.assign_user_role(alice_id, analyst_role_id) is True
    for token in (alice_one.session_token, alice_two.session_token):
        with pytest.raises(IPSPError) as invalidated:
            services.auth_service.authenticate_session(token)
        assert invalidated.value.error_code == "AUTH-SESSION_INVALID"
    assert services.auth_service.authenticate_session(bob.session_token).user_id == bob_id
    with pytest.raises(IPSPError):
        services.rbac_service.assign_user_role(999_999, analyst_role_id)
    with pytest.raises(IPSPError):
        services.rbac_service.assign_user_role(bob_id, 999_999)


def test_role_mapping_change_invalidates_shared_role_only_and_noop_survives(
    rbac_app: FastAPI,
) -> None:
    services = rbac_app.state.foundation_services
    services.rbac_catalog_service.ensure_core_catalog()
    shared_role_id = _add_role(rbac_app, "SharedRole")
    other_role_id = _add_role(rbac_app, "OtherRole")
    first_id = _add_user(rbac_app, "first", shared_role_id)
    second_id = _add_user(rbac_app, "second", shared_role_id)
    other_id = _add_user(rbac_app, "other", other_role_id)
    first = services.auth_service.login("first", PASSWORD)
    second = services.auth_service.login("second", PASSWORD)
    other = services.auth_service.login("other", PASSWORD)

    assert services.rbac_service.replace_role_permissions(shared_role_id, set()) is False
    services.auth_service.authenticate_session(first.session_token)
    assert (
        services.rbac_service.replace_role_permissions(
            shared_role_id, {CorePermission.DATASET_VIEW}
        )
        is True
    )
    for token in (first.session_token, second.session_token):
        with pytest.raises(IPSPError):
            services.auth_service.authenticate_session(token)
    assert services.auth_service.authenticate_session(other.session_token).user_id == other_id
    assert services.rbac_service.has_permission(first_id, CorePermission.DATASET_VIEW)
    assert services.rbac_service.has_permission(second_id, CorePermission.DATASET_VIEW)
    with pytest.raises(IPSPError):
        services.rbac_service.replace_role_permissions(shared_role_id, {"unknown.permission"})


def test_runtime_permission_freshness_across_mapping_changes(rbac_app: FastAPI) -> None:
    services = rbac_app.state.foundation_services
    services.rbac_catalog_service.ensure_core_catalog()
    role_id = _add_role(rbac_app, "RuntimeRole")
    user_id = _add_user(rbac_app, "runtime-user", role_id)
    services.rbac_service.replace_role_permissions(role_id, {CorePermission.DATASET_VIEW})
    allowed_session = services.auth_service.login("runtime-user", PASSWORD)
    assert services.rbac_service.has_permission(user_id, CorePermission.DATASET_VIEW)

    services.rbac_service.replace_role_permissions(role_id, set())
    with pytest.raises(IPSPError):
        services.auth_service.authenticate_session(allowed_session.session_token)
    denied_session = services.auth_service.login("runtime-user", PASSWORD)
    assert not services.rbac_service.has_permission(user_id, CorePermission.DATASET_VIEW)

    services.rbac_service.replace_role_permissions(role_id, {CorePermission.DATASET_VIEW})
    with pytest.raises(IPSPError):
        services.auth_service.authenticate_session(denied_session.session_token)
    services.auth_service.login("runtime-user", PASSWORD)
    assert services.rbac_service.has_permission(user_id, CorePermission.DATASET_VIEW)


def test_catalog_expansion_invalidates_existing_admin_sessions_only(rbac_app: FastAPI) -> None:
    services = rbac_app.state.foundation_services
    admin_role_id = _add_role(rbac_app, "Admin")
    user_role_id = _add_role(rbac_app, "User")
    admin_id = _add_user(rbac_app, "legacy-admin", admin_role_id)
    user_id = _add_user(rbac_app, "legacy-user", user_role_id)
    admin = services.auth_service.login("legacy-admin", PASSWORD)
    user = services.auth_service.login("legacy-user", PASSWORD)

    first = services.rbac_catalog_service.ensure_core_catalog()
    assert first.admin_mappings_created == 13
    assert first.sessions_invalidated_for_users == 1
    with pytest.raises(IPSPError):
        services.auth_service.authenticate_session(admin.session_token)
    assert services.auth_service.authenticate_session(user.session_token).user_id == user_id
    assert services.rbac_service.has_permission(admin_id, CorePermission.SYSTEM_CONFIGURE)

    replacement = services.auth_service.login("legacy-admin", PASSWORD)
    second = services.rbac_catalog_service.ensure_core_catalog()
    assert second.changed is False
    assert second.sessions_invalidated_for_users == 0
    assert services.auth_service.authenticate_session(replacement.session_token).user_id == admin_id


def test_sync_cli_supports_existing_users_and_safe_noop_output(
    rbac_app: FastAPI,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    services = rbac_app.state.foundation_services
    role_id = _add_role(rbac_app, "ExistingRole")
    _add_user(rbac_app, "existing-user", role_id)
    services.database_engine.dispose()

    assert rbac_cli_main() == 0
    first_output = capsys.readouterr().out
    assert "permissions_created=13" in first_output
    assert PASSWORD not in first_output
    assert rbac_cli_main() == 0
    second_output = capsys.readouterr().out
    assert "roles_created=0" in second_output
    assert "permissions_created=0" in second_output
    assert "admin_mappings_created=0" in second_output


def test_sync_refuses_database_below_current_migration_head(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "20260811_02")
    app = create_app(settings)
    try:
        with pytest.raises(IPSPError) as failure:
            synchronize_core_rbac(
                app.state.foundation_services.rbac_catalog_service,
                app.state.foundation_services.migration_state,
            )
    finally:
        app.state.foundation_services.database_engine.dispose()
    assert failure.value.error_code == "AUTHZ-RBAC_INVALID"
    assert "migration head" in failure.value.safe_message


def test_bootstrap_provisions_explicit_admin_authority_and_no_user_grants(
    rbac_app: FastAPI,
) -> None:
    services = rbac_app.state.foundation_services
    admin_id = services.auth_service.bootstrap_admin("first-admin", "First Admin", None, PASSWORD)
    admin = _role(rbac_app, "Admin")
    user = _role(rbac_app, "User")
    with services.database_sessions.session() as session:
        permission_count = session.scalar(select(func.count()).select_from(Permission))
        mapping_count = session.scalar(select(func.count()).select_from(RolePermission))
        user_mapping_count = session.scalar(
            select(func.count())
            .select_from(RolePermission)
            .where(RolePermission.role_id == user.id)
        )
    assert permission_count == 13
    assert mapping_count == 13
    assert user_mapping_count == 0
    assert services.rbac_service.has_permission(admin_id, CorePermission.USER_MANAGE)
    with services.database_sessions.session() as session:
        persisted = session.get(User, admin_id)
        assert persisted is not None and persisted.role_id == admin.id
    with pytest.raises(IPSPError, match="no longer available"):
        services.auth_service.bootstrap_admin("second", "Second", None, PASSWORD)


def test_catalog_absence_does_not_make_readiness_fail(rbac_app: FastAPI) -> None:
    with TestClient(rbac_app, base_url="https://testserver") as client:
        response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    services = rbac_app.state.foundation_services
    assert services.rbac_service.has_permission(999_999, CorePermission.USER_MANAGE) is False


def test_session_schema_has_no_permission_snapshot(rbac_app: FastAPI) -> None:
    assert {
        "permissions",
        "permission_codes",
        "permission_snapshot",
        "role_name",
        "is_admin",
    }.isdisjoint(UserSession.__table__.columns.keys())
