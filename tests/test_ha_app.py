from __future__ import annotations

import tomllib
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
APP_DIR = REPO / "ha-app" / "nibe_service_usb"


def load_app_config() -> dict:
    return yaml.safe_load((APP_DIR / "config.yaml").read_text(encoding="utf-8"))


def test_app_version_matches_gateway_version() -> None:
    # The App's Dockerfile installs the gateway from tag v<App version>.
    pyproject = tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))
    assert load_app_config()["version"] == pyproject["project"]["version"]


def test_app_slug_matches_folder_name() -> None:
    assert load_app_config()["slug"] == APP_DIR.name
