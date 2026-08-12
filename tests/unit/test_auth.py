"""Password, schema-contract, and auth-setting unit tests."""

import logging

import pytest
from ipsp.api.schemas.auth import ChangePasswordRequest, LoginRequest
from ipsp.auth.passwords import MAX_PASSWORD_LENGTH, PasswordInputError, PasswordService
from ipsp.config.settings import AuthSettings, Environment, Settings
from pydantic import ValidationError


def test_password_service_uses_argon2id_and_preserves_unicode() -> None:
    passwords = PasswordService()
    plaintext = "pässwörd-秘密-🔐"

    password_hash = passwords.hash(plaintext)

    assert password_hash != plaintext
    assert password_hash.startswith("$argon2id$")
    assert passwords.verify(plaintext, password_hash) is True
    assert passwords.verify("wrong", password_hash) is False
    assert passwords.verify(plaintext, "not-a-valid-password-hash") is False
    assert passwords.verify_and_update(plaintext, "not-a-valid-password-hash") == (False, None)
    verified, replacement = passwords.verify_and_update(plaintext, password_hash)
    assert verified is True
    assert replacement is None or replacement.startswith("$argon2id$")
    assert not password_hash.startswith(("$2a$", "$2b$", "$2y$"))


def test_password_boundary_rejects_empty_and_oversized_without_trimming() -> None:
    passwords = PasswordService()

    with pytest.raises(PasswordInputError):
        passwords.hash("")
    with pytest.raises(PasswordInputError):
        passwords.hash("x" * (MAX_PASSWORD_LENGTH + 1))

    spaced_hash = passwords.hash(" password ")
    assert passwords.verify(" password ", spaced_hash)
    assert not passwords.verify("password", spaced_hash)


def test_secret_request_fields_do_not_render_plaintext(caplog: pytest.LogCaptureFixture) -> None:
    marker = "DO_NOT_LEAK_LOGIN_PASSWORD"
    login = LoginRequest(username="test", password=marker)
    change = ChangePasswordRequest(current_password=marker, new_password=f"new-{marker}")

    logging.getLogger("ipsp.test").info("schemas=%r %r", login, change)
    rendered = repr(login) + repr(change) + caplog.text

    assert marker not in rendered
    assert "**********" in rendered


def test_auth_settings_defaults_and_validation() -> None:
    auth = AuthSettings()

    assert auth.session_ttl_minutes == 480
    assert auth.failed_login_threshold == 5
    assert auth.lockout_minutes == 15
    assert auth.cookie_secure is True
    assert auth.cookie_samesite == "lax"

    for values in (
        {"session_ttl_minutes": 0},
        {"failed_login_threshold": 0},
        {"lockout_minutes": 0},
        {"session_cookie_name": "bad cookie"},
        {"csrf_header_name": "bad:header"},
        {"session_cookie_name": "same", "csrf_cookie_name": "same"},
        {"cookie_samesite": "none"},
    ):
        with pytest.raises(ValidationError):
            AuthSettings(**values)  # type: ignore[arg-type]


def test_production_rejects_insecure_cookie_and_development_allows_explicit_override() -> None:
    with pytest.raises(ValidationError, match="Secure authentication cookies"):
        Settings(
            _env_file=None,
            environment=Environment.PRODUCTION,
            auth={"cookie_secure": False},
        )

    settings = Settings(
        _env_file=None,
        environment=Environment.DEVELOPMENT,
        auth={"cookie_secure": False},
    )
    assert settings.auth.cookie_secure is False
