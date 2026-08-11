"""SQLite engine, metadata, session, and transaction behavior tests."""

from pathlib import Path

import pytest
from ipsp.config.settings import DatabaseSettings
from ipsp.database.engine import create_database_engine
from ipsp.database.models import Base
from ipsp.database.session import DatabaseSessionFactory
from sqlalchemy import Engine, text


@pytest.fixture
def engine(tmp_path: Path) -> Engine:
    database_engine = create_database_engine(
        DatabaseSettings(url=f"sqlite:///{(tmp_path / 'sessions.db').as_posix()}")
    )
    try:
        with database_engine.begin() as connection:
            connection.execute(text("CREATE TABLE test_records (value TEXT NOT NULL)"))
        yield database_engine
    finally:
        database_engine.dispose()


def _record_count(engine: Engine) -> int:
    with engine.connect() as connection:
        return int(connection.scalar(text("SELECT count(*) FROM test_records")) or 0)


def test_canonical_metadata_starts_without_business_tables() -> None:
    assert dict(Base.metadata.tables) == {}
    assert Base.metadata.naming_convention is not None
    assert Base.metadata.naming_convention["pk"] == "pk_%(table_name)s"


def test_sqlite_foreign_keys_are_enabled_for_every_connection(tmp_path: Path) -> None:
    engine = create_database_engine(
        DatabaseSettings(url=f"sqlite:///{(tmp_path / 'foreign-keys.db').as_posix()}")
    )
    try:
        with engine.connect() as connection:
            assert connection.scalar(text("PRAGMA foreign_keys")) == 1
    finally:
        engine.dispose()


def test_plain_session_does_not_commit_implicitly(engine: Engine) -> None:
    sessions = DatabaseSessionFactory(engine)

    with sessions.session() as session:
        session.execute(text("INSERT INTO test_records (value) VALUES ('uncommitted')"))

    assert _record_count(engine) == 0


def test_explicit_transaction_commits(engine: Engine) -> None:
    sessions = DatabaseSessionFactory(engine)

    with sessions.transaction() as session:
        session.execute(text("INSERT INTO test_records (value) VALUES ('committed')"))

    assert _record_count(engine) == 1


def test_failed_transaction_rolls_back_and_closes(engine: Engine) -> None:
    sessions = DatabaseSessionFactory(engine)

    with (
        pytest.raises(RuntimeError, match="rollback marker"),
        sessions.transaction() as session,
    ):
        session.execute(text("INSERT INTO test_records (value) VALUES ('rolled-back')"))
        raise RuntimeError("rollback marker")

    assert _record_count(engine) == 0
