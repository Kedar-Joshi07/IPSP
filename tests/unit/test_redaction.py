"""Shared structured-data redaction policy tests."""

from ipsp.security.redaction import REDACTED_VALUE, sanitize_structured_data


def test_credential_key_forms_are_redacted_recursively() -> None:
    sanitized = sanitize_structured_data(
        {
            "access_token": "access-value",
            "refresh_token": "refresh-value",
            "client_secret": "client-value",
            "secret_key": "secret-value",
            "x-api-key": "api-value",
            "set-cookie": "cookie-value",
            "Proxy-Authorization": "proxy-value",
            "nested": [
                {"database-password": "password-value"},
                {"service_token": "service-value"},
            ],
        }
    )

    assert isinstance(sanitized, dict)
    assert sanitized == {
        "access_token": REDACTED_VALUE,
        "refresh_token": REDACTED_VALUE,
        "client_secret": REDACTED_VALUE,
        "secret_key": REDACTED_VALUE,
        "x-api-key": REDACTED_VALUE,
        "set-cookie": REDACTED_VALUE,
        "Proxy-Authorization": REDACTED_VALUE,
        "nested": [
            {"database-password": REDACTED_VALUE},
            {"service_token": REDACTED_VALUE},
        ],
    }


def test_unrelated_key_and_token_substrings_remain_intact() -> None:
    sanitized = sanitize_structured_data(
        {
            "monkey_business": "ordinary",
            "keyboard_layout": "qwerty",
            "token_count": 12,
            "secretary": "available",
        }
    )

    assert sanitized == {
        "monkey_business": "ordinary",
        "keyboard_layout": "qwerty",
        "token_count": 12,
        "secretary": "available",
    }
