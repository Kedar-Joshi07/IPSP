"""Secret-provider fail-closed and non-disclosure tests."""

import json
import logging

import pytest
from fastapi.testclient import TestClient
from ipsp.errors.exceptions import IPSPError
from ipsp.main import create_app
from ipsp.observability.logging import JsonFormatter
from ipsp.security.redaction import sanitize_structured_data
from ipsp.security.secrets import EnvironmentSecretProvider, SecretRef, SecretValue
from pydantic import BaseModel, ConfigDict, ValidationError
from pydantic_core import PydanticSerializationError

MARKER = "DO_NOT_LEAK_PHASE1B_SECRET"


class SecretEnvelope(BaseModel):
    """Test-only proof that ordinary Pydantic serialization cannot reveal plaintext."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    value: SecretValue


def _record(metadata: object) -> logging.LogRecord:
    record = logging.LogRecord("ipsp.secret", logging.INFO, __file__, 1, "safe", (), None)
    record.ipsp_metadata = metadata
    return record


def test_optional_missing_secret_returns_none_without_environment_dump() -> None:
    provider = EnvironmentSecretProvider({"UNRELATED_SECRET": MARKER})
    ref = SecretRef(provider="environment", key="MISSING_SECRET")

    assert provider.get(ref) is None
    assert MARKER not in repr(provider)


def test_required_missing_secret_fails_closed_safely() -> None:
    provider = EnvironmentSecretProvider({"UNRELATED_SECRET": MARKER})
    ref = SecretRef(provider="environment", key="MISSING_SECRET")

    with pytest.raises(IPSPError) as caught:
        provider.require(ref)

    assert caught.value.error_code == "SYS-SECRET_REQUIRED"
    assert MARKER not in str(caught.value)
    assert MARKER not in repr(caught.value.details)


def test_environment_secret_requires_explicit_reveal_and_has_safe_equality() -> None:
    provider = EnvironmentSecretProvider({"PROVIDER_API_KEY": MARKER})
    secret = provider.require(SecretRef(provider="environment", key="PROVIDER_API_KEY"))

    assert secret.reveal() == MARKER
    assert secret == SecretValue(MARKER)
    assert MARKER not in repr(secret)
    assert MARKER not in str(secret)


def test_secret_value_is_not_ordinary_json_or_log_plaintext() -> None:
    secret = SecretValue(MARKER)
    envelope = SecretEnvelope(value=secret)

    with pytest.raises(TypeError):
        json.dumps({"value": secret})
    with pytest.raises(PydanticSerializationError) as serialization_error:
        envelope.model_dump_json()

    sanitized = sanitize_structured_data({"value": secret})
    rendered_log = JsonFormatter().format(_record({"value": secret}))
    assert sanitized == {"value": "[UNSUPPORTED]"}
    assert MARKER not in repr(envelope.model_dump())
    assert MARKER not in str(serialization_error.value)
    assert MARKER not in repr(sanitized)
    assert MARKER not in rendered_log


def test_secret_reference_validation_rejects_unsafe_metadata() -> None:
    with pytest.raises(ValidationError):
        SecretRef(provider="Bad Provider", key="SAFE_KEY")
    with pytest.raises(ValidationError):
        SecretRef(provider="environment", key="unsafe key with spaces")


def test_provider_mismatch_is_safe_and_does_not_resolve_value() -> None:
    provider = EnvironmentSecretProvider({"PROVIDER_API_KEY": MARKER})
    ref = SecretRef(provider="future-vault", key="PROVIDER_API_KEY")

    with pytest.raises(IPSPError) as caught:
        provider.require(ref)

    assert caught.value.error_code == "SYS-SECRET_PROVIDER"
    assert MARKER not in str(caught.value)
    assert MARKER not in repr(caught.value.details)


def test_secret_marker_cannot_escape_through_api_error_details(settings) -> None:  # type: ignore[no-untyped-def]
    provider = EnvironmentSecretProvider({"PROVIDER_API_KEY": MARKER})
    secret = provider.require(SecretRef(provider="environment", key="PROVIDER_API_KEY"))
    app = create_app(settings)

    def fail() -> None:
        raise IPSPError(
            "SYS-SECRET_TEST",
            "Secret resolution failed safely.",
            details={"resolved_value": secret},
        )

    app.add_api_route("/api/v1/test/secret-error", fail)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/test/secret-error")

    assert response.status_code == 500
    assert response.json()["details"] == {"resolved_value": "[UNSUPPORTED]"}
    assert MARKER not in response.text
