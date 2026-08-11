"""SQLite engine, metadata, session, and transaction behavior tests."""

import logging
from pathlib import Path

import pytest
from ipsp.config.settings import DatabaseSettings
from ipsp.database.engine import create_database_engine
from ipsp.database.models import Base
from ipsp.database.session import DatabaseSessionFactory
from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError, StatementError


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


def test_canonical_metadata_contains_only_phase1d_security_tables() -> None:
    assert set(Base.metadata.tables) == {"permissions", "role_permissions", "roles", "users"}
    assert Base.metadata.naming_convention is not None
    assert Base.metadata.naming_convention["pk"] == "pk_%(table_name)s"


def test_sqlite_foreign_keys_are_enabled_for_every_connection(tmp_path: Path) -> None:
    engine = create_database_engine(
        DatabaseSettings(url=f"sqlite:///{(tmp_path / 'foreign-keys.db').as_posix()}")
    )
    try:
        with engine.connect() as connection:
            assert connection.scalar(text("PRAGMA foreign_keys")) == 1
            first_driver_connection = connection.connection.driver_connection
        engine.dispose()
        with engine.connect() as connection:
            assert connection.scalar(text("PRAGMA foreign_keys")) == 1
            second_driver_connection = connection.connection.driver_connection
        assert second_driver_connection is not first_driver_connection
    finally:
        engine.dispose()


def test_sqlite_foreign_key_constraint_rejects_invalid_child(tmp_path: Path) -> None:
    engine = create_database_engine(
        DatabaseSettings(url=f"sqlite:///{(tmp_path / 'foreign-key-constraint.db').as_posix()}")
    )
    try:
        with engine.begin() as connection:
            connection.execute(text("CREATE TABLE test_parents (id INTEGER PRIMARY KEY)"))
            connection.execute(
                text(
                    "CREATE TABLE test_children ("
                    "id INTEGER PRIMARY KEY, "
                    "parent_id INTEGER NOT NULL REFERENCES test_parents(id))"
                )
            )

        with pytest.raises(IntegrityError), engine.begin() as connection:
            connection.execute(
                text("INSERT INTO test_children (id, parent_id) VALUES (:id, :parent_id)"),
                {"id": 1, "parent_id": 999},
            )
    finally:
        engine.dispose()


def test_sqlalchemy_logging_and_errors_hide_bound_parameters(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    marker = "DO_NOT_LEAK_DATABASE_PARAMETER"
    engine = create_database_engine(
        DatabaseSettings(
            url=f"sqlite:///{(tmp_path / 'parameter-privacy.db').as_posix()}",
            echo=True,
        )
    )
    try:
        with (
            caplog.at_level(logging.INFO, logger="sqlalchemy.engine.Engine"),
            engine.connect() as connection,
            pytest.raises(StatementError) as failure,
        ):
            connection.execute(
                text("SELECT value FROM missing_table WHERE value = :value"),
                {"value": marker},
            )
    finally:
        engine.dispose()

    captured = capsys.readouterr()
    rendered = caplog.text + captured.out + captured.err + str(failure.value)
    assert "SQL parameters hidden" in rendered
    assert marker not in rendered


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
