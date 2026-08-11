"""Phase 1A architecture and contamination guardrails."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND = PROJECT_ROOT / "backend" / "ipsp"
FRONTEND = PROJECT_ROOT / "frontend"


def _read_production_source() -> str:
    paths = list(BACKEND.rglob("*.py"))
    paths.extend(
        path for path in FRONTEND.rglob("*") if path.suffix.lower() in {".html", ".css", ".js"}
    )
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_production_source_has_no_prohibited_architecture_patterns() -> None:
    source = _read_production_source()
    lowered = source.lower()

    assert "streamlit" not in lowered
    assert "session.query(" not in lowered
    assert "python-jose" not in lowered
    assert "jsonwebtoken" not in lowered
    for network_import in (
        "import requests",
        "import httpx",
        "from httpx",
        "import aiohttp",
        "urllib.request",
    ):
        assert network_import not in lowered


def test_generic_core_has_no_benchmark_specific_output_terms() -> None:
    lowered = _read_production_source().lower()

    for term in ("campaignsim", "campaign", "funnel_stage", "roas", "cpa", "faiss", "xgboost"):
        assert term not in lowered


def test_frontend_has_no_runtime_cdn_reference() -> None:
    lowered = _read_production_source().lower()

    for term in ("cdnjs", "unpkg.com", "jsdelivr.net"):
        assert term not in lowered
