"""Structured-log redaction and explicit envelope-extension tests."""

import json
import logging

from ipsp.observability.logging import JsonFormatter, sanitize_metadata


def _record(**extras: object) -> logging.LogRecord:
    record = logging.LogRecord(
        name="ipsp.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="Safe structured event",
        args=(),
        exc_info=None,
    )
    for key, value in extras.items():
        setattr(record, key, value)
    return record


def test_sensitive_metadata_is_redacted_recursively() -> None:
    sanitized = sanitize_metadata(
        {
            "user": "safe",
            "access_token": "hidden",
            "nested": [
                {"refresh_token": "hidden", "client_secret": "hidden"},
                {"secret_key": "hidden", "x-api-key": "hidden", "set-cookie": "hidden"},
            ],
        }
    )

    assert sanitized == {
        "user": "safe",
        "access_token": "[REDACTED]",
        "nested": [
            {"refresh_token": "[REDACTED]", "client_secret": "[REDACTED]"},
            {"secret_key": "[REDACTED]", "x-api-key": "[REDACTED]", "set-cookie": "[REDACTED]"},
        ],
    }


def test_formatter_omits_absent_optional_context_fields() -> None:
    payload = json.loads(JsonFormatter().format(_record()))

    for field in (
        "session_correlation_id",
        "user_id",
        "resolved_role",
        "duration_ms",
        "error_code",
        "resource_type",
        "resource_id",
        "project_id",
        "dataset_id",
        "model_id",
        "run_id",
    ):
        assert field not in payload


def test_formatter_emits_only_allowlisted_optional_context_fields() -> None:
    payload = json.loads(
        JsonFormatter().format(
            _record(
                ipsp_session_correlation_id="session-correlation-1",
                ipsp_user_id="user-1",
                ipsp_resolved_role="viewer",
                ipsp_duration_ms=12.5,
                ipsp_error_code="SYS-TEST",
                ipsp_resource_type="project",
                ipsp_resource_id="resource-1",
                ipsp_project_id="project-1",
                ipsp_dataset_version_id="dataset-version-1",
                ipsp_model_version_id="model-version-1",
                ipsp_run_id="run-1",
                ipsp_metadata={"access_token": "hidden", "normal": "visible"},
                ipsp_arbitrary_extra="must-not-be-serialized",
            )
        )
    )

    assert payload["session_correlation_id"] == "session-correlation-1"
    assert payload["user_id"] == "user-1"
    assert payload["resolved_role"] == "viewer"
    assert payload["duration_ms"] == 12.5
    assert payload["error_code"] == "SYS-TEST"
    assert payload["resource_type"] == "project"
    assert payload["resource_id"] == "resource-1"
    assert payload["project_id"] == "project-1"
    assert payload["dataset_version_id"] == "dataset-version-1"
    assert payload["model_version_id"] == "model-version-1"
    assert payload["run_id"] == "run-1"
    assert payload["metadata"] == {"access_token": "[REDACTED]", "normal": "visible"}
    assert "ipsp_arbitrary_extra" not in payload
    assert "arbitrary_extra" not in payload
