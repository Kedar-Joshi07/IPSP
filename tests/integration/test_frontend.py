"""Phase 1J offline frontend, browser-client, and security contracts."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi.testclient import TestClient
from ipsp.config.settings import Environment, Settings
from ipsp.main import create_app

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND = PROJECT_ROOT / "frontend"
PRODUCTION_EXTENSIONS = {".html", ".css", ".js"}


def _frontend_files() -> list[Path]:
    return sorted(
        path
        for path in FRONTEND.rglob("*")
        if path.is_file() and path.suffix.lower() in PRODUCTION_EXTENSIONS
    )


def _production_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in _frontend_files())


def test_frontend_and_known_assets_are_served_without_shadowing_apis(tmp_path: Path) -> None:
    settings = Settings(
        _env_file=None,
        environment=Environment.TEST,
        frontend_dir=FRONTEND,
        data_dir=tmp_path / "data",
        artifacts_dir=tmp_path / "artifacts",
        log_dir=tmp_path / "logs",
        database={"url": f"sqlite:///{(tmp_path / 'frontend.db').as_posix()}"},
    )
    app = create_app(settings)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            index = client.get("/")
            css = client.get("/css/tokens.css")
            javascript = client.get("/js/app.js")
            api = client.get("/api/v1")
            live = client.get("/health/live")
            ready = client.get("/health/ready")

        assert index.status_code == css.status_code == javascript.status_code == 200
        assert "text/html" in index.headers["content-type"]
        assert "text/css" in css.headers["content-type"]
        assert "javascript" in javascript.headers["content-type"]
        assert api.status_code == live.status_code == 200
        assert ready.status_code == 503
        assert api.json()["name"] == "IPSP"
        assert live.json()["status"] == "alive"
        assert ready.json()["status"] == "not_ready"
    finally:
        app.state.foundation_services.database_engine.dispose()


def test_index_is_accessible_semantic_local_shell() -> None:
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")

    assert '<a class="skip-link" href="#main-content">' in html
    assert '<header class="topbar"' in html
    assert '<nav class="primary-navigation"' in html
    assert '<main class="main" id="main-content"' in html
    assert "<noscript>" in html
    assert "CampaignSim" in html and "Powered by IPSP" in html
    assert "Intelligent Predictive Simulation Platform" in html
    assert 'aria-hidden="true"' in html
    assert "onclick=" not in html.lower()
    assert re.findall(r'<script[^>]+src="([^"]+)"', html) == ["/js/app.js"]
    assert all(url.startswith("/") for url in re.findall(r'<link[^>]+href="([^"]+)"', html))


def test_themes_have_matching_complete_semantic_variable_sets() -> None:
    dark = (FRONTEND / "css" / "theme-dark.css").read_text(encoding="utf-8")
    light = (FRONTEND / "css" / "theme-light.css").read_text(encoding="utf-8")

    def variables(source: str) -> set[str]:
        return set(re.findall(r"--[a-z0-9-]+(?=\s*:)", source))

    assert variables(dark) == variables(light)
    assert len(variables(dark)) >= 25
    assert "--color-bg: #0a0b0e" in dark
    assert ':root[data-theme="light"]' in light
    assert "color-scheme: dark" in dark
    assert "color-scheme: light" in light


def test_responsive_motion_and_print_contracts_exist() -> None:
    base = (FRONTEND / "css" / "base.css").read_text(encoding="utf-8")
    responsive = (FRONTEND / "css" / "responsive.css").read_text(encoding="utf-8")
    print_css = (FRONTEND / "css" / "print.css").read_text(encoding="utf-8")

    assert "prefers-reduced-motion: reduce" in base
    assert "max-width: 68.6875rem" in responsive
    assert "max-width: 47.9375rem" in responsive
    assert "max-width: 29.9375rem" in responsive
    assert ".sidebar" in responsive and "translateX" in responsive
    assert "@page" in print_css
    assert ".topbar" in print_css and ".sidebar" in print_css
    assert "background: #ffffff" in print_css


def test_frontend_has_no_unsafe_dom_or_code_execution_sinks() -> None:
    source = _production_text()
    lowered = source.lower()
    for prohibited in (
        ".innerhtml",
        ".outerhtml",
        "insertadjacenthtml",
        "document.write",
        "eval(",
        "new function",
    ):
        assert prohibited not in lowered

    dom_source = (FRONTEND / "js" / "dom.js").read_text(encoding="utf-8")
    assert "textContent" in dom_source
    assert "createTextNode" in dom_source
    assert "createElement" in dom_source
    for hostile_value in (
        "<img src=x onerror=alert(1)>",
        "<script>DO_NOT_EXECUTE</script>",
        '"><svg/onload=alert(1)>',
    ):
        assert hostile_value not in source


def test_storage_and_cookie_access_are_strictly_owned() -> None:
    javascript = list((FRONTEND / "js").rglob("*.js"))
    local_storage_files = [
        path for path in javascript if "localStorage" in path.read_text(encoding="utf-8")
    ]
    cookie_files = [
        path for path in javascript if "document.cookie" in path.read_text(encoding="utf-8")
    ]
    source = "\n".join(path.read_text(encoding="utf-8") for path in javascript)

    assert local_storage_files == [FRONTEND / "js" / "theme.js"]
    assert cookie_files == [FRONTEND / "js" / "api.js"]
    assert 'const STORAGE_KEY = "ipsp.theme"' in local_storage_files[0].read_text(encoding="utf-8")
    assert "sessionStorage" not in source
    assert "session_token" not in source.lower()
    assert "csrf_token" not in source.lower()


def test_api_client_uses_browser_config_and_correct_csrf_boundaries() -> None:
    source = (FRONTEND / "js" / "api.js").read_text(encoding="utf-8")

    assert 'credentials: "same-origin"' in source
    assert "if (response.status === 204)" in source
    assert "browserConfig.csrf_cookie_name" in source
    assert "browserConfig.csrf_header_name" in source
    assert "ipsp_csrf" not in source
    assert "X-CSRF-Token" not in source
    assert 'login(username, password) { return request("/api/v1/auth/login", '
    assert (
        'logout() { return request("/api/v1/auth/logout", { method: "POST", csrf: true })' in source
    )
    assert (
        "changePassword(currentPassword, newPassword) { return "
        'request("/api/v1/auth/change-password", { method: "POST", csrf: true'
    ) in source
    assert (
        "cancelJob(jobId) { return request(`"
        '/api/v1/jobs/${encodeURIComponent(jobId)}/cancel`, { method: "POST", csrf: true })'
    ) in source
    assert (
        "retryJob(jobId) { return request(`"
        '/api/v1/jobs/${encodeURIComponent(jobId)}/retry`, { method: "POST", csrf: true })'
    ) in source
    for get_function in ("getReadiness", "getCurrentUser", "listJobs", "getJob", "getSystemHealth"):
        line = next(line for line in source.splitlines() if f"function {get_function}" in line)
        assert "csrf: true" not in line


def test_jobs_and_system_health_ui_match_current_server_contracts() -> None:
    jobs = (FRONTEND / "js" / "views" / "jobs.js").read_text(encoding="utf-8")
    health = (FRONTEND / "js" / "views" / "system-health.js").read_text(encoding="utf-8")

    assert set(re.findall(r'"(QUEUED|RUNNING|SUCCEEDED|FAILED|CANCELLED)"', jobs)) == {
        "QUEUED",
        "RUNNING",
        "SUCCEEDED",
        "FAILED",
        "CANCELLED",
    }
    assert "submitJob" not in jobs and "createJob" not in jobs
    assert "Job submission is not available" in jobs
    assert "getJob(" in jobs and "cancelJob(" in jobs and "retryJob(" in jobs
    assert "if (loading) return" in jobs
    assert set(
        re.findall(
            r'"(healthy|degraded|unhealthy|not_configured|not_implemented|not_available|not_initialized|never_run)"',
            health,
        )
    ) == {
        "healthy",
        "degraded",
        "unhealthy",
        "not_configured",
        "not_implemented",
        "not_available",
        "not_initialized",
        "never_run",
    }
    assert "error?.status === 403" in health
    assert "role_name" not in health and '"Admin"' not in health
    assert "getSystemHealth()" in health
    assert "getReadiness()" not in health
    assert "if (loading) return" in health


def test_frontend_is_offline_framework_free_and_not_demo_contaminated() -> None:
    source = _production_text()
    lowered = source.lower()

    assert "https://" not in lowered and "http://" not in lowered
    for prohibited in (
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "unpkg",
        "jsdelivr",
        "cdnjs",
        "plotly",
        "jquery",
        "tailwind",
        "streamlit",
    ):
        assert prohibited not in lowered
    for framework_pattern in (r"\breact\b", r"\bvue\b", r"\bangular\b", r"\bsvelte\b"):
        assert re.search(framework_pattern, lowered) is None
    for demo_term in (
        "summer acquisition",
        "climatewear",
        "target roas",
        "historical similarity",
        "search + social",
        "ad fatigue",
        "roas",
        "cpa",
        "ctr",
        "bf1",
        "bf2",
        "bf3",
        "bf4",
        "bf5",
        "bf6",
        "bf7",
        "bf8",
    ):
        assert demo_term not in lowered
    assert "CampaignSim" in source
