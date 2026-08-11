"""Lightweight offline frontend structure tests."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND = PROJECT_ROOT / "frontend"


def test_frontend_has_accessible_application_shell() -> None:
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")

    assert '<main class="main" id="main-content">' in html
    assert 'id="theme-toggle"' in html
    assert 'aria-live="polite"' in html
    assert "Intelligent Predictive Simulation Platform" in html
    assert 'aria-label="IPSP home"' in html


def test_dark_and_light_theme_foundations_exist() -> None:
    dark = (FRONTEND / "css" / "theme-dark.css").read_text(encoding="utf-8")
    light = (FRONTEND / "css" / "theme-light.css").read_text(encoding="utf-8")
    theme_js = (FRONTEND / "js" / "theme.js").read_text(encoding="utf-8")

    assert "--color-bg: #0a0b0e" in dark
    assert ':root[data-theme="light"]' in light
    assert "localStorage" in theme_js
    assert "matchMedia" in theme_js


def test_frontend_is_offline_and_has_no_public_asset_urls() -> None:
    production_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".html", ".css", ".js"}
    )

    assert "https://" not in production_text
    assert "http://" not in production_text
    assert "cdnjs" not in production_text.lower()
