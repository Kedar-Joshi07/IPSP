"""Argon2id password hashing at the authentication boundary."""

from pwdlib import PasswordHash
from pwdlib.exceptions import PwdlibError

MAX_PASSWORD_LENGTH = 1_024
_DUMMY_PASSWORD = "ipsp-non-secret-unknown-user-timing-value"
_DUMMY_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$"
    "hB9zCsN6QWt9dYx1c2iGvg$A6d67TRVc6WgWsH/0oU+4Aj/7wYOBsHD5KCFpRiz4kU"
)


class PasswordInputError(ValueError):
    """Password input is empty or too large for safe hashing."""


class PasswordService:
    """Hash and verify passwords using pwdlib's recommended Argon2id policy."""

    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    @staticmethod
    def validate(password: str) -> None:
        if not password or len(password) > MAX_PASSWORD_LENGTH:
            raise PasswordInputError("Password input is invalid")

    def hash(self, password: str) -> str:
        self.validate(password)
        return self._password_hash.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        self.validate(password)
        try:
            return self._password_hash.verify(password, password_hash)
        except PwdlibError:
            return False

    def verify_and_update(self, password: str, password_hash: str) -> tuple[bool, str | None]:
        self.validate(password)
        try:
            return self._password_hash.verify_and_update(password, password_hash)
        except PwdlibError:
            return False, None

    def equalize_unknown_user(self, password: str) -> None:
        """Perform one real Argon2 verification without permitting authentication."""
        candidate = password if 0 < len(password) <= MAX_PASSWORD_LENGTH else _DUMMY_PASSWORD
        self._password_hash.verify(candidate, _DUMMY_HASH)
