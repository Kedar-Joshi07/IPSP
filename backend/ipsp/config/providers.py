"""Explicit construction of configured Phase 1B foundation services."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy import Engine

from ipsp.auth.passwords import PasswordService
from ipsp.auth.rbac import RBACCatalogService, RBACService
from ipsp.auth.service import AuthService
from ipsp.config.feature_flags import FeatureFlags
from ipsp.config.settings import Settings
from ipsp.database.engine import create_database_engine
from ipsp.database.migrations import MigrationStateService, canonical_migrations_path
from ipsp.database.session import DatabaseSessionFactory
from ipsp.observability.audit import AuditService
from ipsp.security.outbound import OutboundPolicy
from ipsp.security.secrets import EnvironmentSecretProvider, SecretProvider
from ipsp.services.readiness import ReadinessService


@dataclass(frozen=True, slots=True)
class FoundationServices:
    """Immutable composition result injected at the application boundary."""

    settings: Settings
    feature_flags: FeatureFlags
    secret_provider: SecretProvider
    outbound_policy: OutboundPolicy
    database_engine: Engine
    database_sessions: DatabaseSessionFactory
    migration_state: MigrationStateService
    readiness_service: ReadinessService
    password_service: PasswordService
    audit_service: AuditService
    auth_service: AuthService
    rbac_service: RBACService
    rbac_catalog_service: RBACCatalogService


def build_foundation_services(
    settings: Settings,
    *,
    environ: Mapping[str, str] | None = None,
) -> FoundationServices:
    """Construct Phase 1B services without mutable globals or provider side effects."""
    secret_provider = EnvironmentSecretProvider(environ)
    outbound = settings.outbound
    outbound_policy = OutboundPolicy(
        internet_enabled=outbound.internet_enabled,
        remote_llm_enabled=outbound.remote_llm_enabled,
        remote_llm_feature_enabled=settings.features.remote_llm_enabled,
        allowed_remote_providers=outbound.allowed_remote_providers,
        model_download_enabled=outbound.model_download_enabled,
        update_check_enabled=outbound.update_check_enabled,
        default_transmission_level=outbound.default_remote_transmission,
    )
    database_engine = create_database_engine(settings.database)
    database_sessions = DatabaseSessionFactory(database_engine)
    migration_state = MigrationStateService(database_engine, canonical_migrations_path())
    readiness_service = ReadinessService(settings, database_engine, migration_state)
    password_service = PasswordService()
    audit_service = AuditService(database_sessions)
    auth_service = AuthService(settings.auth, database_sessions, password_service, audit_service)
    rbac_service = RBACService(database_sessions, audit_service)
    rbac_catalog_service = RBACCatalogService(database_sessions, audit_service)
    return FoundationServices(
        settings=settings,
        feature_flags=settings.features,
        secret_provider=secret_provider,
        outbound_policy=outbound_policy,
        database_engine=database_engine,
        database_sessions=database_sessions,
        migration_state=migration_state,
        readiness_service=readiness_service,
        password_service=password_service,
        audit_service=audit_service,
        auth_service=auth_service,
        rbac_service=rbac_service,
        rbac_catalog_service=rbac_catalog_service,
    )
