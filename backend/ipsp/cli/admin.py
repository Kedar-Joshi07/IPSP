"""Interactive one-time bootstrap for the first IPSP administrator."""

from __future__ import annotations

import getpass

from ipsp.auth.service import AuthService
from ipsp.config.providers import build_foundation_services
from ipsp.config.settings import Settings
from ipsp.database.migrations import MigrationStateService
from ipsp.errors.exceptions import IPSPError


def bootstrap_first_admin(
    auth_service: AuthService,
    migration_state: MigrationStateService,
    *,
    username: str,
    display_name: str,
    email: str | None,
    password: str,
) -> int:
    """Create the first admin only when the database is already at migration head."""
    if not migration_state.inspect().at_head:
        raise IPSPError(
            "AUTH-BOOTSTRAP_UNAVAILABLE",
            "Admin bootstrap requires the database to be at the current migration head.",
        )
    return auth_service.bootstrap_admin(username, display_name, email, password)


def main() -> int:
    """Prompt without echoing password material and perform one bootstrap attempt."""
    settings = Settings()
    services = build_foundation_services(settings)
    try:
        username = input("Username: ")
        display_name = input("Display name: ")
        email_input = input("Email (optional): ")
        password = getpass.getpass("Password: ")
        confirmation = getpass.getpass("Confirm password: ")
        if not password or password != confirmation:
            print("Admin bootstrap failed: password confirmation did not match.")
            return 1
        user_id = bootstrap_first_admin(
            services.auth_service,
            services.migration_state,
            username=username,
            display_name=display_name,
            email=email_input or None,
            password=password,
        )
    except IPSPError as exc:
        print(f"Admin bootstrap failed: {exc.safe_message}")
        return 1
    finally:
        services.database_engine.dispose()
    print(f"Administrator created with user ID {user_id}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
