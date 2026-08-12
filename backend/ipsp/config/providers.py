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
from ipsp.jobs.contracts import JobHandler
from ipsp.jobs.enums import JobType
from ipsp.jobs.executor import JobExecutor
from ipsp.jobs.local import LocalJobBackend
from ipsp.jobs.service import JobService
from ipsp.observability.audit import AuditService
from ipsp.security.outbound import OutboundPolicy
from ipsp.security.secrets import EnvironmentSecretProvider, SecretProvider
from ipsp.services.readiness import ReadinessService
from ipsp.services.system_health import SystemHealthService


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
    system_health_service: SystemHealthService
    password_service: PasswordService
    audit_service: AuditService
    auth_service: AuthService
    rbac_service: RBACService
    rbac_catalog_service: RBACCatalogService
    job_executor: JobExecutor
    job_backend: LocalJobBackend
    job_service: JobService


def build_foundation_services(
    settings: Settings,
    *,
    environ: Mapping[str, str] | None = None,
    job_handlers: Mapping[JobType, JobHandler] | None = None,
) -> FoundationServices:
    """Construct current foundation services without mutable globals or runtime side effects."""
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
    password_service = PasswordService()
    audit_service = AuditService(database_sessions)
    auth_service = AuthService(settings.auth, database_sessions, password_service, audit_service)
    rbac_service = RBACService(database_sessions, audit_service)
    rbac_catalog_service = RBACCatalogService(database_sessions, audit_service)
    job_executor = JobExecutor(database_sessions, audit_service, job_handlers)
    job_backend = LocalJobBackend(job_executor)
    job_service = JobService(database_sessions, job_backend, audit_service)
    readiness_service = ReadinessService(
        settings,
        database_engine,
        migration_state,
        job_backend,
    )
    system_health_service = SystemHealthService(
        settings,
        database_engine,
        database_sessions,
        migration_state,
        readiness_service,
        job_backend,
        outbound_policy,
    )
    return FoundationServices(
        settings=settings,
        feature_flags=settings.features,
        secret_provider=secret_provider,
        outbound_policy=outbound_policy,
        database_engine=database_engine,
        database_sessions=database_sessions,
        migration_state=migration_state,
        readiness_service=readiness_service,
        system_health_service=system_health_service,
        password_service=password_service,
        audit_service=audit_service,
        auth_service=auth_service,
        rbac_service=rbac_service,
        rbac_catalog_service=rbac_catalog_service,
        job_executor=job_executor,
        job_backend=job_backend,
        job_service=job_service,
    )
