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
        "changePassword(currentPassword, newPassword, signal) { return "
        'request("/api/v1/auth/change-password", { method: "POST", csrf: true'
    ) in source
    assert (
        "cancelJob(jobId, signal) { return request(`"
        '/api/v1/jobs/${encodeURIComponent(jobId)}/cancel`, { method: "POST", csrf: true'
    ) in source
    assert (
        "retryJob(jobId, signal) { return request(`"
        '/api/v1/jobs/${encodeURIComponent(jobId)}/retry`, { method: "POST", csrf: true'
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
    assert "if (loading || !isActive()) return" in jobs
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
    assert "getSystemHealth(context.signal)" in health
    assert "getReadiness()" not in health
    assert "if (loading || !isActive()) return" in health


def test_router_has_one_abortable_generation_guarded_lifecycle() -> None:
    router = (FRONTEND / "js" / "router.js").read_text(encoding="utf-8")

    assert "new AbortController()" in router
    assert "const routeGeneration = ++generation" in router
    assert "generation === routeGeneration" in router
    assert "activeController.abort()" in router
    assert "cleanupActiveRoute()" in router
    assert "const once = (callback)" in router
    assert "if (called) return" in router
    assert "if (cleanup) cleanup()" in router
    dispatch = router[router.index("const dispatch") : router.index("const onHashChange")]
    assert dispatch.index("activeController.abort()") < dispatch.index("await onRoute")
    stale_guard = "generation !== routeGeneration || controller.signal.aborted"
    assert dispatch.index("await onRoute") < dispatch.index(stale_guard)
    assert dispatch.index(stale_guard) < dispatch.index("activeCleanup = cleanup")


def test_app_preserves_view_cleanup_and_never_bypasses_router_for_refresh() -> None:
    app = (FRONTEND / "js" / "app.js").read_text(encoding="utf-8")

    assert "cleanup = await renderOverview" in app
    assert "cleanup = await renderJobs" in app
    assert "cleanup = await renderSystemHealth" in app
    assert "return cleanup" in app
    assert "refresh: () => router?.refresh()" in app
    assert "void renderRoute(" not in app
    assert "window.render" not in app


def test_stale_async_views_use_route_signal_and_activity_guards() -> None:
    views = FRONTEND / "js" / "views"
    login = (views / "login.js").read_text(encoding="utf-8")
    overview = (views / "overview.js").read_text(encoding="utf-8")
    jobs = (views / "jobs.js").read_text(encoding="utf-8")
    health = (views / "system-health.js").read_text(encoding="utf-8")

    assert "getReadiness(context.signal)" in login
    assert "login(username.value, password.value, context.signal)" in login
    assert "!active || !context.isActive()" in login
    assert "getReadiness(context.signal)" in overview
    assert "listJobs(5, 0, context.signal)" in overview
    assert "if (!isActive()) return" in overview
    for source in (jobs, health):
        assert "context.signal" in source
        assert "context.isRouteAbort(error)" in source
        assert "if (isActive())" in source


def test_system_theme_always_tracks_operating_system_preference() -> None:
    theme = (FRONTEND / "js" / "theme.js").read_text(encoding="utf-8")

    assert "preference = storedPreference() ?? configuredDefault" in theme
    assert 'if (value === "dark" || value === "light") return value' in theme
    assert 'value === "system" && configuredDefault' not in theme
    assert 'if (preference === "system") apply()' in theme


def test_readiness_accepts_only_valid_ready_or_not_ready_documents() -> None:
    api = (FRONTEND / "js" / "api.js").read_text(encoding="utf-8")

    assert "parseResponse(response, [503])" in api
    assert 'responseStatus === 200 ? "ready" : "not_ready"' in api
    assert "Date.parse(payload.timestamp_utc)" in api
    assert "response.status !== 200 && response.status !== 503" in api
    assert "isReadinessPayload(payload, response.status)" in api
    assert 'new ApiError(0, "SYS-REQUEST-FAILED"' in api
    assert '"SYS-RESPONSE-INVALID"' in api


def test_login_and_overview_distinguish_valid_not_ready_from_failure() -> None:
    login = (FRONTEND / "js" / "views" / "login.js").read_text(encoding="utf-8")
    overview = (FRONTEND / "js" / "views" / "overview.js").read_text(encoding="utf-8")

    assert "Local service ready" in login
    assert "Local service not ready" in login
    assert "Local readiness unavailable" in login
    assert "The platform reports that it is not ready." in overview
    assert "Promise.all" in overview


def test_job_actions_match_authoritative_retry_and_cancel_boundaries() -> None:
    jobs = (FRONTEND / "js" / "views" / "jobs.js").read_text(encoding="utf-8")

    assert 'job.status === "QUEUED"' in jobs
    assert 'job.status === "RUNNING" && job.cancel_requested !== true' in jobs
    assert 'job.status === "FAILED" || job.status === "CANCELLED"' in jobs
    assert "job.retryable === true" in jobs
    assert "job.attempt_count < job.max_attempts" in jobs


def test_job_detail_clears_busy_state_before_final_redraw() -> None:
    jobs = (FRONTEND / "js" / "views" / "jobs.js").read_text(encoding="utf-8")
    load_detail = jobs[jobs.index("const loadDetail") : jobs.index("const mutate")]

    assert "busyId = null" in load_detail
    assert "if (shouldDraw && isActive()) draw()" in load_detail
    final_draw = load_detail.index("draw()", load_detail.index("finally"))
    assert load_detail.index("busyId = null") < final_draw


def test_jobs_cleanup_owns_and_closes_only_its_dialogs() -> None:
    jobs = (FRONTEND / "js" / "views" / "jobs.js").read_text(encoding="utf-8")

    assert "const dialogs = new Set()" in jobs
    assert "dialogs.add(dialog)" in jobs
    assert "dialogs.delete(dialog)" in jobs
    assert "if (dialog.open) dialog.close()" in jobs
    assert 'document.querySelectorAll("dialog")' not in jobs


def test_required_password_view_has_centralized_duplicate_safe_signout() -> None:
    app = (FRONTEND / "js" / "app.js").read_text(encoding="utf-8")
    profile = (FRONTEND / "js" / "views" / "profile.js").read_text(encoding="utf-8")

    assert 'button("Sign out"' in profile
    assert "await context.onLogout()" in profile
    assert "if (signOut.disabled) return" in profile
    assert "if (loggingOut) return" in app
    assert "onLogout: performLogout" in app


def test_auth_transitions_use_one_same_hash_aware_helper() -> None:
    app = (FRONTEND / "js" / "app.js").read_text(encoding="utf-8")
    helper = app[app.index("function transitionAfterAuth") : app.index("function showLogin")]

    assert "if (!navigate(target)) router?.refresh()" in helper
    assert helper.count("navigate(") == 1
    assert helper.count("router?.refresh()") == 1
    assert app.count("transitionAfterAuth(") == 5
    assert "const changed = navigate(" not in app


def test_required_password_identity_renders_when_url_is_already_login() -> None:
    app = (FRONTEND / "js" / "app.js").read_text(encoding="utf-8")
    render = app[app.index("async function renderRoute") : app.index("async function bootstrap")]

    required_branch = "if (identity?.must_change_password)"
    authenticated_login_branch = 'else if (identity && route.key === "login")'
    assert render.index(required_branch) < render.index(authenticated_login_branch)
    assert "renderRequiredPassword" in render


def test_logout_and_successful_password_change_force_actual_login_render() -> None:
    app = (FRONTEND / "js" / "app.js").read_text(encoding="utf-8")
    logout = app[app.index("async function performLogout") : app.index("function viewContext")]
    password_changed = app[app.index("onPasswordChanged:") : app.index("onLogout: performLogout")]

    for transition in (logout, password_changed):
        assert "clearIdentity()" in transition
        assert 'transitionAfterAuth("#/login")' in transition
        assert transition.index("clearIdentity()") < transition.index("transitionAfterAuth")


def test_change_password_401_uses_centralized_auth_transition_before_form_error() -> None:
    profile = (FRONTEND / "js" / "views" / "profile.js").read_text(encoding="utf-8")
    catch = profile[
        profile.index("} catch (error) {") : profile.index(
            "} finally {", profile.index("} catch (error) {")
        )
    ]

    stale_guard = "context.isRouteAbort(error) || !active || !context.isActive()"
    auth_guard = "if (context.handleAuthError(error)) return"
    form_error = "notices.append(alertBox"
    assert catch.index(stale_guard) < catch.index(auth_guard) < catch.index(form_error)


def test_auth_transitions_do_not_duplicate_route_render_or_cleanup() -> None:
    app = (FRONTEND / "js" / "app.js").read_text(encoding="utf-8")

    assert "void renderRoute(" not in app
    assert "renderRoute({" not in app
    assert "router?.refresh();\n  navigate(" not in app
    assert "const changed = navigate(" not in app


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
