"""Structured-log redaction and explicit envelope-extension tests."""

import json
import logging
from pathlib import Path

from ipsp.observability.events import EventStream, new_event
from ipsp.observability.logging import JsonFormatter, configure_logging, sanitize_metadata


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
                ipsp_user_id=1,
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
    assert payload["user_id"] == 1
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


def test_event_streams_and_generated_envelope_are_exact() -> None:
    assert {stream.value for stream in EventStream} == {
        "audit",
        "security",
        "application",
        "frontend",
        "data_processing",
        "ml",
        "llm",
        "simulation",
        "performance",
        "export",
        "errors",
        "system",
    }
    event = new_event(
        stream=EventStream.SYSTEM,
        component="test",
        action="test.generated",
        status="success",
        severity="INFO",
    )
    assert event.event_id
    assert event.trace_id
    assert event.request_id
    assert event.timestamp_utc.utcoffset() is not None


def test_formatter_emits_bounded_structure_without_exception_secrets(tmp_path: Path) -> None:
    message_marker = "DO_NOT_LEAK_EXCEPTION_MESSAGE"
    arg_marker = "DO_NOT_LEAK_EXCEPTION_ARG"
    local_marker = "DO_NOT_LEAK_EXCEPTION_LOCAL"
    absolute_marker = str(tmp_path / "DO_NOT_LEAK_ABSOLUTE_PATH")

    try:
        local_secret = local_marker
        raise RuntimeError(message_marker, arg_marker, absolute_marker, local_secret)
    except RuntimeError:
        record = logging.LogRecord(
            name="ipsp.test",
            level=logging.ERROR,
            pathname=absolute_marker,
            lineno=99,
            msg="Safe unexpected error",
            args=(),
            exc_info=__import__("sys").exc_info(),
        )

    rendered = JsonFormatter().format(record)
    payload = json.loads(rendered)
    assert payload["exception_type"] == "RuntimeError"
    assert 1 <= len(payload["exception_frames"]) <= 32
    assert set(payload["exception_frames"][-1]) == {"file_name", "function", "line_number"}
    assert all(
        "/" not in frame["file_name"] and "\\" not in frame["file_name"]
        for frame in payload["exception_frames"]
    )
    for marker in (
        message_marker,
        arg_marker,
        local_marker,
        absolute_marker,
        "Traceback (most recent call last)",
    ):
        assert marker not in rendered


def test_rotating_jsonl_reconfigures_without_touching_unrelated_handlers(tmp_path: Path) -> None:
    logger = logging.getLogger("ipsp")
    unrelated = logging.NullHandler()
    logger.addHandler(unrelated)
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    try:
        configure_logging("INFO", first_dir, max_bytes=180, backup_count=2)
        logger.info("Safe rotation event", extra={"ipsp_metadata": {"password": "hidden"}})
        first_size = (first_dir / "ipsp-runtime.jsonl").stat().st_size

        configure_logging("INFO", second_dir, max_bytes=180, backup_count=2)
        for _ in range(8):
            logger.info("Safe rotation event", extra={"ipsp_metadata": {"password": "hidden"}})

        assert unrelated in logger.handlers
        assert (first_dir / "ipsp-runtime.jsonl").stat().st_size == first_size
        files = sorted(second_dir.glob("ipsp-runtime.jsonl*"))
        assert 1 <= len(files) <= 3
        for path in files:
            for line in path.read_text(encoding="utf-8").splitlines():
                payload = json.loads(line)
                assert payload["metadata"]["password"] == "[REDACTED]"
                assert payload["event_id"] and payload["trace_id"] and payload["request_id"]
    finally:
        logger.removeHandler(unrelated)
        for handler in list(logger.handlers):
            if getattr(handler, "ipsp_handler", False):
                logger.removeHandler(handler)
                handler.close()
