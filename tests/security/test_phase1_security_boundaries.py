"""Phase 1K static-host containment and cross-surface privacy proofs."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
from ipsp.config.settings import Environment, Settings
from ipsp.main import create_app


def test_static_host_is_contained_and_does_not_shadow_api_error_or_health_contracts(
    tmp_path: Path,
) -> None:
    frontend = tmp_path / "public"
    (frontend / "css").mkdir(parents=True)
    (frontend / "js").mkdir()
    (frontend / "index.html").write_text("<h1>IPSP_PHASE1K_PUBLIC_SHELL</h1>", encoding="utf-8")
    (frontend / "css" / "app.css").write_text("body { color: black; }", encoding="utf-8")
    (frontend / "js" / "app.js").write_text("'use strict';", encoding="utf-8")
    private_marker = "PHASE1K_STATIC_PARENT_DO_NOT_LEAK"
    (tmp_path / "private-marker.txt").write_text(private_marker, encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=PHASE1K_ENV_DO_NOT_LEAK", encoding="utf-8")
    settings = Settings(
        _env_file=None,
        environment=Environment.TEST,
        frontend_dir=frontend,
        data_dir=tmp_path / "data",
        artifacts_dir=tmp_path / "artifacts",
        log_dir=tmp_path / "logs",
        database={"url": f"sqlite:///{(tmp_path / 'private.db').as_posix()}"},
    )
    app = create_app(settings)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            assert client.get("/").text == "<h1>IPSP_PHASE1K_PUBLIC_SHELL</h1>"
            assert client.get("/css/app.css").status_code == 200
            assert client.get("/js/app.js").status_code == 200
            assert client.get("/api/v1").headers["content-type"].startswith("application/json")
            assert client.get("/health/live").json()["status"] == "alive"

            ready = client.get("/health/ready", headers={"X-Trace-ID": "phase1k-ready"})
            assert ready.status_code == 503
            assert set(ready.json()) == {
                "status",
                "timestamp_utc",
                "checks",
                "deferred_checks",
                "error_code",
            }

            unauthorized = client.get(
                "/api/v1/admin/system/health",
                headers={"X-Trace-ID": "phase1k-auth-trace"},
            )
            assert unauthorized.status_code == 401
            assert unauthorized.json()["error_code"] == "AUTH-SESSION_REQUIRED"
            assert unauthorized.json()["trace_id"] == unauthorized.headers["X-Trace-ID"]
            assert {"error_code", "message", "trace_id", "recoverable", "details"} == set(
                unauthorized.json()
            )

            responses = [
                client.get("/private-marker.txt"),
                client.get("/../private-marker.txt"),
                client.get("/%2e%2e/private-marker.txt"),
                client.get("/..%2fprivate-marker.txt"),
                client.get("/%2e%2e%5cprivate-marker.txt"),
                client.get("/.env"),
                client.get("/private.db"),
                client.get("/logs/ipsp-runtime.jsonl"),
            ]
            assert all(response.status_code != 200 for response in responses)
            combined = "\n".join(response.text for response in responses)
            assert private_marker not in combined
            assert "PHASE1K_ENV_DO_NOT_LEAK" not in combined
            assert str(tmp_path) not in combined
            assert "Traceback" not in combined
    finally:
        app.state.foundation_services.database_engine.dispose()
