"""Read-only inspection of the canonical Alembic migration state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic.util.exc import CommandError
from sqlalchemy import Engine


class MigrationStateError(RuntimeError):
    """Safe boundary error for unavailable or invalid migration history."""


@dataclass(frozen=True, slots=True)
class MigrationState:
    """Database revision compared with the sole expected Alembic head."""

    current_revision: str | None
    expected_head: str
    at_head: bool


def canonical_migrations_path() -> Path:
    """Resolve the repository's frozen single Alembic history root."""
    return Path(__file__).resolve().parents[3] / "database" / "migrations"


class MigrationStateService:
    """Inspect migration state without upgrading or mutating the schema."""

    def __init__(self, engine: Engine, migrations_path: Path) -> None:
        self._engine = engine
        self._migrations_path = migrations_path

    def expected_head(self) -> str:
        config = Config()
        config.set_main_option("script_location", str(self._migrations_path))
        try:
            head = ScriptDirectory.from_config(config).get_current_head()
        except (CommandError, OSError) as exc:
            raise MigrationStateError("Migration history is unavailable") from exc
        if head is None:
            raise MigrationStateError("Migration history has no expected head")
        return head

    def inspect(self) -> MigrationState:
        expected_head = self.expected_head()
        with self._engine.connect() as connection:
            current_revision = MigrationContext.configure(connection).get_current_revision()
        return MigrationState(
            current_revision=current_revision,
            expected_head=expected_head,
            at_head=current_revision == expected_head,
        )
