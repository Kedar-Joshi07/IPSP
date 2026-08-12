"""Phase 1D security schema, ORM, constraint, and UTC integration tests."""

from collections.abc import Iterator
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from ipsp.config.settings import Settings
from ipsp.database.engine import create_database_engine
from ipsp.database.models import Permission, Role, RolePermission, User, UserSession
from ipsp.database.session import DatabaseSessionFactory
from sqlalchemy import Engine, inspect, select, text
from sqlalchemy.exc import IntegrityError, StatementError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_TABLES = {
    "alembic_version",
    "audit_events",
    "jobs",
    "permissions",
    "role_permissions",
    "roles",
    "user_sessions",
    "users",
}
USER_COLUMNS = {
    "id",
    "username",
    "display_name",
    "email",
    "password_hash",
    "role_id",
    "is_active",
    "must_change_password",
    "failed_login_count",
    "locked_until",
    "last_login_at",
    "password_changed_at",
    "created_at",
    "created_by",
    "updated_at",
}
TEST_PASSWORD_HASH = "TEST_HASH_NOT_A_REAL_PASSWORD"


@pytest.fixture
def security_engine(
    settings: Settings,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[Engine]:
    monkeypatch.setenv("IPSP_DATABASE__URL", settings.database.url)
    command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
    engine = create_database_engine(settings.database)
    try:
        yield engine
    finally:
        engine.dispose()


def _new_user(username: str, role_id: int, **values: object) -> User:
    return User(
        username=username,
        display_name=f"Test {username}",
        email=None,
        password_hash=TEST_PASSWORD_HASH,
        role_id=role_id,
        **values,
    )


def _insert_role(engine: Engine, name: str = "test-role") -> int:
    sessions = DatabaseSessionFactory(engine)
    with sessions.transaction() as session:
        role = Role(name=name, description=None)
        session.add(role)
        session.flush()
        return role.id


def _insert_role_and_permission(engine: Engine) -> tuple[int, int]:
    sessions = DatabaseSessionFactory(engine)
    with sessions.transaction() as session:
        role = Role(name="test-role", description=None)
        permission = Permission(code="simulation.run", description=None)
        session.add_all((role, permission))
        session.flush()
        return role.id, permission.id


def test_migrated_schema_is_exact_and_has_no_seed_rows(security_engine: Engine) -> None:
    inspector = inspect(security_engine)

    assert set(inspector.get_table_names()) == EXPECTED_TABLES
    with security_engine.connect() as connection:
        for table in EXPECTED_TABLES - {"alembic_version"}:
            assert connection.scalar(text(f"SELECT count(*) FROM {table}")) == 0


def test_users_schema_matches_frozen_columns_constraints_and_defaults(
    security_engine: Engine,
) -> None:
    inspector = inspect(security_engine)
    columns = {column["name"]: column for column in inspector.get_columns("users")}
    unique_columns = {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints("users")
    }
    foreign_keys = {
        (
            tuple(foreign_key["constrained_columns"]),
            foreign_key["referred_table"],
            tuple(foreign_key["referred_columns"]),
        )
        for foreign_key in inspector.get_foreign_keys("users")
    }
    checks = {constraint["sqltext"] for constraint in inspector.get_check_constraints("users")}

    assert set(columns) == USER_COLUMNS
    assert columns["email"]["nullable"] is True
    assert columns["created_by"]["nullable"] is True
    for required in USER_COLUMNS - {"email", "locked_until", "last_login_at", "created_by"}:
        assert columns[required]["nullable"] is False
    for defaulted in {
        "is_active",
        "must_change_password",
        "failed_login_count",
        "password_changed_at",
        "created_at",
        "updated_at",
    }:
        assert columns[defaulted]["default"] is not None
    assert unique_columns == {("username",)}
    assert foreign_keys == {
        (("role_id",), "roles", ("id",)),
        (("created_by",), "users", ("id",)),
    }
    assert any("failed_login_count >= 0" in check for check in checks)


def test_user_sessions_schema_is_hash_only_and_enforces_user_foreign_key(
    security_engine: Engine,
) -> None:
    inspector = inspect(security_engine)
    columns = {column["name"]: column for column in inspector.get_columns("user_sessions")}
    assert set(columns) == {
        "id",
        "token_hash",
        "csrf_token_hash",
        "session_correlation_id",
        "user_id",
        "created_at",
        "last_seen_at",
        "expires_at",
        "invalidated_at",
    }
    assert columns["invalidated_at"]["nullable"] is True
    assert all(not columns[name]["nullable"] for name in set(columns) - {"invalidated_at"})
    assert {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints("user_sessions")
    } == {("token_hash",), ("session_correlation_id",)}
    assert {
        (
            tuple(foreign_key["constrained_columns"]),
            foreign_key["referred_table"],
            tuple(foreign_key["referred_columns"]),
        )
        for foreign_key in inspector.get_foreign_keys("user_sessions")
    } == {(("user_id",), "users", ("id",))}
    assert {index["name"] for index in inspector.get_indexes("user_sessions")} == {
        "ix_user_sessions_user_id"
    }
    assert all(term not in columns for term in {"token", "csrf_token", "jwt", "refresh_token"})

    now = datetime.now(UTC)
    sessions = DatabaseSessionFactory(security_engine)
    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(
            UserSession(
                token_hash="a" * 64,
                csrf_token_hash="b" * 64,
                session_correlation_id="00000000-0000-4000-8000-000000000000",
                user_id=999,
                created_at=now,
                last_seen_at=now,
                expires_at=now + timedelta(hours=1),
                invalidated_at=None,
            )
        )


def test_role_permission_schema_has_composite_key_and_exact_foreign_keys(
    security_engine: Engine,
) -> None:
    inspector = inspect(security_engine)
    primary_key = inspector.get_pk_constraint("role_permissions")
    foreign_keys = {
        (
            tuple(foreign_key["constrained_columns"]),
            foreign_key["referred_table"],
            tuple(foreign_key["referred_columns"]),
        )
        for foreign_key in inspector.get_foreign_keys("role_permissions")
    }

    assert primary_key["constrained_columns"] == ["role_id", "permission_id"]
    assert foreign_keys == {
        (("role_id",), "roles", ("id",)),
        (("permission_id",), "permissions", ("id",)),
    }


def test_role_and_permission_uniqueness_and_nullable_descriptions(
    security_engine: Engine,
) -> None:
    inspector = inspect(security_engine)
    role_columns = {column["name"]: column for column in inspector.get_columns("roles")}
    permission_columns = {column["name"]: column for column in inspector.get_columns("permissions")}

    assert role_columns["description"]["nullable"] is True
    assert permission_columns["description"]["nullable"] is True
    assert {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints("roles")
    } == {("name",)}
    assert {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints("permissions")
    } == {("code",)}


def test_orm_insert_query_and_explicit_authorization_structure_join(
    security_engine: Engine,
) -> None:
    sessions = DatabaseSessionFactory(security_engine)
    with sessions.transaction() as session:
        role = Role(name="analyst", description="Test role")
        permission = Permission(code="simulation.run", description="Test permission")
        session.add_all((role, permission))
        session.flush()
        session.add(RolePermission(role_id=role.id, permission_id=permission.id))
        user = _new_user("schema-user", role.id)
        session.add(user)
        session.flush()
        user_id = user.id

    with sessions.session() as session:
        persisted = session.execute(select(User).where(User.id == user_id)).scalar_one()
        permission_codes = session.scalars(
            select(Permission.code)
            .select_from(User)
            .join(Role, User.role_id == Role.id)
            .join(RolePermission, RolePermission.role_id == Role.id)
            .join(Permission, Permission.id == RolePermission.permission_id)
            .where(User.id == user_id)
        ).all()

    assert persisted.email is None
    assert persisted.is_active is True
    assert persisted.must_change_password is True
    assert persisted.failed_login_count == 0
    assert persisted.locked_until is None
    assert persisted.last_login_at is None
    for timestamp in (
        persisted.password_changed_at,
        persisted.created_at,
        persisted.updated_at,
    ):
        assert timestamp.tzinfo is UTC
    assert permission_codes == ["simulation.run"]


def test_aware_offset_timestamps_normalize_and_round_trip_as_utc(
    security_engine: Engine,
) -> None:
    role_id = _insert_role(security_engine)
    sessions = DatabaseSessionFactory(security_engine)
    offset = timezone(timedelta(hours=5, minutes=30))
    local_timestamp = datetime(2026, 8, 11, 12, 30, tzinfo=offset)
    expected_utc = local_timestamp.astimezone(UTC)
    with sessions.transaction() as session:
        user = _new_user(
            "timezone-user",
            role_id,
            locked_until=local_timestamp,
            last_login_at=local_timestamp,
            password_changed_at=local_timestamp,
            created_at=local_timestamp,
            updated_at=local_timestamp,
        )
        session.add(user)
        session.flush()
        user_id = user.id

    with sessions.session() as session:
        persisted = session.get(User, user_id)

    assert persisted is not None
    for timestamp in (
        persisted.locked_until,
        persisted.last_login_at,
        persisted.password_changed_at,
        persisted.created_at,
        persisted.updated_at,
    ):
        assert timestamp == expected_utc
        assert timestamp.tzinfo is UTC


def test_naive_security_timestamp_is_rejected(security_engine: Engine) -> None:
    role_id = _insert_role(security_engine)
    sessions = DatabaseSessionFactory(security_engine)

    with (
        pytest.raises(StatementError, match="timezone-aware"),
        sessions.transaction() as session,
    ):
        session.add(
            _new_user(
                "naive-time-user",
                role_id,
                password_changed_at=datetime(2026, 8, 11, 12, 30),
            )
        )


def test_duplicate_username_is_rejected(security_engine: Engine) -> None:
    role_id = _insert_role(security_engine)
    sessions = DatabaseSessionFactory(security_engine)
    with sessions.transaction() as session:
        session.add(_new_user("duplicate-user", role_id))

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(_new_user("duplicate-user", role_id))


def test_duplicate_role_name_is_rejected(security_engine: Engine) -> None:
    _insert_role(security_engine, "duplicate-role")
    sessions = DatabaseSessionFactory(security_engine)

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(Role(name="duplicate-role", description=None))


def test_duplicate_permission_code_is_rejected(security_engine: Engine) -> None:
    sessions = DatabaseSessionFactory(security_engine)
    with sessions.transaction() as session:
        session.add(Permission(code="dataset.view", description=None))

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(Permission(code="dataset.view", description=None))


def test_duplicate_role_permission_mapping_is_rejected(security_engine: Engine) -> None:
    role_id, permission_id = _insert_role_and_permission(security_engine)
    sessions = DatabaseSessionFactory(security_engine)
    with sessions.transaction() as session:
        session.add(RolePermission(role_id=role_id, permission_id=permission_id))

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(RolePermission(role_id=role_id, permission_id=permission_id))


@pytest.mark.parametrize("invalid_role", (True, False))
def test_role_permission_foreign_keys_are_enforced(
    security_engine: Engine,
    invalid_role: bool,
) -> None:
    role_id, permission_id = _insert_role_and_permission(security_engine)
    sessions = DatabaseSessionFactory(security_engine)

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(
            RolePermission(
                role_id=999 if invalid_role else role_id,
                permission_id=permission_id if invalid_role else 999,
            )
        )


def test_user_role_foreign_key_is_enforced(security_engine: Engine) -> None:
    sessions = DatabaseSessionFactory(security_engine)

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(_new_user("missing-role-user", 999))


def test_user_created_by_self_foreign_key_is_enforced(security_engine: Engine) -> None:
    role_id = _insert_role(security_engine)
    sessions = DatabaseSessionFactory(security_engine)

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(_new_user("missing-creator-user", role_id, created_by=999))


def test_negative_failed_login_count_is_rejected(security_engine: Engine) -> None:
    role_id = _insert_role(security_engine)
    sessions = DatabaseSessionFactory(security_engine)

    with pytest.raises(IntegrityError), sessions.transaction() as session:
        session.add(_new_user("negative-counter-user", role_id, failed_login_count=-1))
