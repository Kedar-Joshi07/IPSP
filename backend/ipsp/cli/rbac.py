"""Explicit existing-installation synchronization for the core RBAC catalog."""

from ipsp.auth.rbac import CatalogSyncResult, RBACCatalogService
from ipsp.config.providers import build_foundation_services
from ipsp.config.settings import Settings
from ipsp.database.migrations import MigrationStateService
from ipsp.errors.exceptions import IPSPError


def synchronize_core_rbac(
    catalog_service: RBACCatalogService,
    migration_state: MigrationStateService,
) -> CatalogSyncResult:
    """Synchronize only when the existing database is already at migration head."""
    if not migration_state.inspect().at_head:
        raise IPSPError(
            "AUTHZ-RBAC_INVALID",
            "RBAC synchronization requires the database to be at the current migration head.",
        )
    return catalog_service.ensure_core_catalog()


def main() -> int:
    """Run additive synchronization and print only non-secret counts."""
    services = build_foundation_services(Settings())
    try:
        result = synchronize_core_rbac(
            services.rbac_catalog_service,
            services.migration_state,
        )
    except IPSPError as exc:
        print(f"RBAC synchronization failed: {exc.safe_message}")
        return 1
    finally:
        services.database_engine.dispose()
    print(
        "RBAC synchronization complete: "
        f"roles_created={result.roles_created}, "
        f"permissions_created={result.permissions_created}, "
        f"admin_mappings_created={result.admin_mappings_created}, "
        f"session_users_invalidated={result.sessions_invalidated_for_users}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
