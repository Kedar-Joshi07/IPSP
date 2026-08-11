"""Establish the schema-free Phase 1C migration baseline.

Revision ID: 20260811_01
Revises: None
Create Date: 2026-08-11
"""

from collections.abc import Sequence

revision: str = "20260811_01"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Record the foundation baseline without creating business tables."""


def downgrade() -> None:
    """Remove the foundation revision marker without dropping business tables."""
