"""Explicit synchronous SQLAlchemy engine construction."""

from sqlalchemy import Engine, event
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.pool import ConnectionPoolEntry

from ipsp.config.settings import DatabaseSettings


def create_database_engine(settings: DatabaseSettings) -> Engine:
    """Create an unconnected SQLite engine with required connection behavior."""
    engine = create_engine(
        settings.url,
        echo=settings.echo,
        hide_parameters=True,
        connect_args={
            "check_same_thread": False,
            "timeout": settings.connection_timeout_seconds,
        },
    )

    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(
        dbapi_connection: DBAPIConnection,
        _connection_record: ConnectionPoolEntry,
    ) -> None:
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
        finally:
            cursor.close()

    return engine
