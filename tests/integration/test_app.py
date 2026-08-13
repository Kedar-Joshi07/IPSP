"""FastAPI factory, probes, errors, and correlation integration tests."""

import json
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from ipsp.api.schemas.common import ErrorResponse
from ipsp.config.settings import Settings
from ipsp.errors.exceptions import IPSPError
from ipsp.main import create_app
from ipsp.observability import context as request_context


def test_factory_builds_application_and_versioned_api(settings: Settings) -> None:
    app = create_app(settings)
    assert isinstance(app, FastAPI)
    assert app.state.foundation_services.settings is settings
    assert app.state.foundation_services.feature_flags is settings.features

    with TestClient(app) as client:
        response = client.get("/api/v1")

    assert response.status_code == 200
    assert response.json() == {
        "name": "IPSP",
        "version": "0.1.0",
        "status": "foundation",
        "browser": {
            "default_theme": "system",
            "csrf_cookie_name": "ipsp_csrf",
            "csrf_header_name": "X-CSRF-Token",
        },
    }


def test_api_root_returns_only_custom_safe_browser_configuration(tmp_path) -> None:
    settings = Settings(
        _env_file=None,
        default_theme="light",
        frontend_dir=tmp_path / "missing-frontend",
        data_dir=tmp_path / "data",
        artifacts_dir=tmp_path / "artifacts",
        log_dir=tmp_path / "logs",
        database={"url": f"sqlite:///{(tmp_path / 'browser-config.db').as_posix()}"},
        auth={
            "csrf_cookie_name": "custom_csrf_cookie",
            "csrf_header_name": "X-Custom-CSRF",
        },
    )
    app = create_app(settings)

    with TestClient(app) as client:
        response = client.get("/api/v1")

    assert response.status_code == 200
    assert response.json() == {
        "name": "IPSP",
        "version": "0.1.0",
        "status": "foundation",
        "browser": {
            "default_theme": "light",
            "csrf_cookie_name": "custom_csrf_cookie",
            "csrf_header_name": "X-Custom-CSRF",
        },
    }
    rendered = response.text.lower()
    for private_term in (
        "session_cookie",
        "session_token",
        "csrf_token",
        "password",
        "secret",
        "database",
        "sqlite",
        "environment",
    ):
        assert private_term not in rendered


def test_liveness_returns_minimal_safe_response(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "alive"
    assert set(response.json()) == {"status", "timestamp_utc"}


def test_readiness_reports_only_active_and_deferred_checks(client: TestClient) -> None:
    response = client.get("/health/ready")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["error_code"] is None
    assert body["checks"] == {
        "application": "ready",
        "configuration": "ready",
        "database": "ready",
        "foreign_keys": "ready",
        "migration": "ready",
        "runtime_logs": "ready",
        "job_worker": "ready",
    }
    assert body["deferred_checks"] == ["analytical_storage"]


def test_trace_and_request_ids_are_propagated(client: TestClient) -> None:
    response = client.get(
        "/health/live",
        headers={"X-Trace-ID": "trace-test-001", "X-Request-ID": "request-test-001"},
    )

    assert response.headers["X-Trace-ID"] == "trace-test-001"
    assert response.headers["X-Request-ID"] == "request-test-001"


def test_domain_error_uses_central_safe_envelope(settings: Settings) -> None:
    app = create_app(settings)

    def forbidden() -> None:
        raise IPSPError("AUTHZ-TEST", "Permission denied")

    app.add_api_route("/api/v1/test/forbidden", forbidden)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/test/forbidden")

    assert response.status_code == 403
    error = ErrorResponse.model_validate(response.json())
    assert error.error_code == "AUTHZ-TEST"
    assert error.message == "Permission denied"
    assert error.trace_id == response.headers["X-Trace-ID"]


def test_domain_error_redacts_nested_unsafe_details(settings: Settings) -> None:
    class UnsafeDetail:
        def __str__(self) -> str:
            return "unsafe-object-secret"

    failure = IPSPError(
        "SYS-SAFE_DETAILS",
        "The request failed safely.",
        details={
            "password": "password-value",
            "nested": [
                {"access_token": "access-value"},
                {"client_secret": "client-value", "opaque": UnsafeDetail()},
            ],
            "normal": "visible",
        },
    )
    assert failure.details is not None
    failure.details["refresh_token"] = "late-mutation-value"

    def fail_safely() -> None:
        raise failure

    app = create_app(settings)
    app.add_api_route("/api/v1/test/safe-details", fail_safely)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/test/safe-details")

    assert response.status_code == 500
    details = response.json()["details"]
    assert details == {
        "password": "[REDACTED]",
        "nested": [
            {"access_token": "[REDACTED]"},
            {"client_secret": "[REDACTED]", "opaque": "[UNSUPPORTED]"},
        ],
        "normal": "visible",
        "refresh_token": "[REDACTED]",
    }
    for unsafe_value in (
        "password-value",
        "access-value",
        "client-value",
        "late-mutation-value",
        "unsafe-object-secret",
    ):
        assert unsafe_value not in response.text


def test_unexpected_error_never_exposes_traceback(settings: Settings) -> None:
    app = create_app(settings)

    def explode() -> None:
        local_marker = "DO_NOT_LEAK_UNEXPECTED_LOCAL"
        raise RuntimeError(
            "DO_NOT_LEAK_UNEXPECTED_MESSAGE",
            "DO_NOT_LEAK_UNEXPECTED_ARG",
            str(settings.log_dir / "DO_NOT_LEAK_UNEXPECTED_PATH"),
            local_marker,
        )

    app.add_api_route("/api/v1/test/explode", explode)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/v1/test/explode")

    assert response.status_code == 500
    assert response.json()["error_code"] == "SYS-UNEXPECTED"
    for marker in (
        "DO_NOT_LEAK_UNEXPECTED_MESSAGE",
        "DO_NOT_LEAK_UNEXPECTED_ARG",
        "DO_NOT_LEAK_UNEXPECTED_LOCAL",
        "DO_NOT_LEAK_UNEXPECTED_PATH",
    ):
        assert marker not in response.text
    assert "Traceback" not in response.text
    assert response.headers["X-Trace-ID"]
    runtime_events = [
        json.loads(line)
        for line in (settings.log_dir / "ipsp-runtime.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    unexpected = next(
        event for event in reversed(runtime_events) if event["action"] == "exception.unexpected"
    )
    assert unexpected["exception_type"] == "RuntimeError"
    assert unexpected["exception_frames"]
    assert set(unexpected["exception_frames"][-1]) == {"file_name", "function", "line_number"}
    rendered = json.dumps(unexpected)
    for marker in (
        "DO_NOT_LEAK_UNEXPECTED_MESSAGE",
        "DO_NOT_LEAK_UNEXPECTED_ARG",
        "DO_NOT_LEAK_UNEXPECTED_LOCAL",
        "DO_NOT_LEAK_UNEXPECTED_PATH",
        "Traceback (most recent call last)",
    ):
        assert marker not in rendered


def test_request_log_status_is_success_for_2xx(client: TestClient) -> None:
    with patch.object(request_context.logger, "info") as request_log:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert request_log.call_args.kwargs["extra"]["ipsp_status"] == "success"
    assert request_log.call_args.kwargs["extra"]["ipsp_metadata"]["status_code"] == 200


def test_request_log_status_is_failure_for_error_response(client: TestClient) -> None:
    with patch.object(request_context.logger, "info") as request_log:
        response = client.get("/api/v1/not-found")

    assert response.status_code == 404
    assert request_log.call_args.kwargs["extra"]["ipsp_status"] == "failure"
    assert request_log.call_args.kwargs["extra"]["ipsp_metadata"]["status_code"] == 404
