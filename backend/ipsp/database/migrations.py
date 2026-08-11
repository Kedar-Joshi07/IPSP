"""Read-only inspection of the canonical Alembic migration state."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from alembic.script.revision import RevisionError
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
            heads = ScriptDirectory.from_config(config).get_heads()
        except (CommandError, OSError, RevisionError) as exc:
            raise MigrationStateError("Migration history is unavailable") from exc
        if len(heads) != 1:
            raise MigrationStateError("Migration history must have exactly one head")
        return heads[0]

    def inspect(self) -> MigrationState:
        expected_head = self.expected_head()
        with self._engine.connect() as connection:
            current_heads = MigrationContext.configure(connection).get_current_heads()
        if len(current_heads) > 1:
            raise MigrationStateError("Database has unexpected multiple migration heads")
        current_revision = current_heads[0] if current_heads else None
        return MigrationState(
            current_revision=current_revision,
            expected_head=expected_head,
            at_head=current_revision == expected_head,
        )
