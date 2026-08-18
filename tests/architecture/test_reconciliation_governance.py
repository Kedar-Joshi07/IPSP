"""F2-I version and license-governance reconciliation checks."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

from ipsp import __version__
from ipsp.config.settings import Settings

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_v011_application_version_surfaces_are_consistent() -> None:
    project = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    env_example = (PROJECT_ROOT / ".env.example").read_text(encoding="utf-8")
    frontend = (PROJECT_ROOT / "frontend" / "index.html").read_text(encoding="utf-8")

    assert __version__ == "0.1.1"
    assert Settings(_env_file=None).app_version == __version__
    assert project["project"]["version"] == __version__
    assert f"IPSP_APP_VERSION={__version__}" in env_example
    assert f"IPSP v{__version__} foundation" in frontend


def test_project_license_and_locked_dependency_inventory_are_complete() -> None:
    project_license = (PROJECT_ROOT / "LICENSE").read_text(encoding="utf-8")
    inventory = (PROJECT_ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
    lock_lines = (PROJECT_ROOT / "requirements.lock").read_text(encoding="utf-8").splitlines()
    locked = {
        name.lower(): version
        for line in lock_lines
        if (match := re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s]+)", line))
        for name, version in [match.groups()]
    }
    inventoried = {
        name.strip().lower(): version.strip()
        for name, version in re.findall(
            r"^\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", inventory, re.MULTILINE
        )
        if name.strip().lower() not in {"package", "---"}
    }

    assert "proprietary" in project_license.lower()
    assert "third-party" in project_license.lower()
    assert inventoried == locked
