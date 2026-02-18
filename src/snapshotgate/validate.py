from __future__ import annotations

from typing import Any

from .utils import safe_div


def _profiles_by_name(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {p["name"]: p for p in profile.get("profiles", [])}



