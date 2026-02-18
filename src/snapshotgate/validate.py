from __future__ import annotations

from typing import Any

from .utils import safe_div


def _profiles_by_name(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {p["name"]: p for p in profile.get("profiles", [])}



def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    uni = len(a | b)
    return safe_div(inter, uni)



def validate(contract: dict[str, Any], new_profile: dict[str, Any]) -> dict[str, Any]:
    base = contract["baseline"]
    th = contract["thresholds"]

    base_cols = set(base.get("columns", []))
    new_cols = set(new_profile.get("columns", []))

    missing = sorted(list(base_cols - new_cols))
    added = sorted(list(new_cols - base_cols))

    base_p = _profiles_by_name(base)
    new_p = _profiles_by_name(new_profile)

    type_changes = []
    per_col = []

    base_rc = float(base.get("row_count", 0) or 0)
    new_rc = float(new_profile.get("row_count", 0) or 0)
    rc_ratio = safe_div(new_rc, base_rc) if base_rc else 1.0
    row_count_ok = (rc_ratio >= th["row_count_min_ratio"]) and (rc_ratio <= th["row_count_max_ratio"])
