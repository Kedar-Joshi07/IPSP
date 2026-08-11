"""Explicit synchronous SQLAlchemy session and transaction lifecycles."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSessionFactory:
    """Create short-lived sessions without implicit commits."""

    def __init__(self, engine: Engine) -> None:
        self._maker = sessionmaker(bind=engine, expire_on_commit=False)

    @contextmanager
    def session(self) -> Iterator[Session]:
        """Yield a session and always close it; never commit implicitly."""
        session = self._maker()
        try:
            yield session
        finally:
            session.close()

    @contextmanager
    def transaction(self) -> Iterator[Session]:
        """Commit one explicit unit of work or roll it back on failure."""
        with self.session() as session, session.begin():
            yield session
