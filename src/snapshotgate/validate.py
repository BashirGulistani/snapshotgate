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

    for col in sorted(list(base_cols & new_cols)):
        b = base_p.get(col)
        n = new_p.get(col)
        if not b or not n:
            continue

        if b["inferred_type"] != n["inferred_type"]:
            type_changes.append({"column": col, "from": b["inferred_type"], "to": n["inferred_type"]})

        b_null = float(b.get("null_rate", 0.0) or 0.0)
        n_null = float(n.get("null_rate", 0.0) or 0.0)
        null_inc = n_null - b_null

        b_unique = float(b.get("unique_approx", 0) or 0)
        n_unique = float(n.get("unique_approx", 0) or 0)
        b_ur = safe_div(b_unique, float(base.get("row_count", 1) or 1))
        n_ur = safe_div(n_unique, float(new_profile.get("row_count", 1) or 1))
        ur_change = safe_div(abs(n_ur - b_ur), (b_ur if b_ur else 1.0))

        b_top = set([kv[0] for kv in (b.get("top_values") or [])])
        n_top = set([kv[0] for kv in (n.get("top_values") or [])])
        jac = jaccard(b_top, n_top)
        jac_drop = 1.0 - jac

        numeric_flag = False
        numeric_detail = None
        if b["inferred_type"] == "number" and n["inferred_type"] == "number":
            b_mean = float((b.get("numeric") or {}).get("mean", 0.0) or 0.0)
            n_mean = float((n.get("numeric") or {}).get("mean", 0.0) or 0.0)
            b_std = float((b.get("numeric") or {}).get("std", 0.0) or 0.0)
            z = safe_div(abs(n_mean - b_mean), (b_std if b_std else 1.0))
            numeric_detail = {"base_mean": b_mean, "new_mean": n_mean, "base_std": b_std, "mean_z": z}
            numeric_flag = z > float(th["max_numeric_mean_z"])

        violations = []
        if null_inc > float(th["max_null_rate_increase"]):
            violations.append({"kind": "null_rate_spike", "base": b_null, "new": n_null, "delta": null_inc})
        if ur_change > float(th["max_unique_rate_change"]):
            violations.append({"kind": "unique_rate_drift", "base": b_ur, "new": n_ur, "ratio": ur_change})
        if jac_drop > float(th["max_top_value_jaccard_drop"]):
            violations.append({"kind": "top_values_drift", "jaccard": jac, "drop": jac_drop})
        if numeric_flag:
            violations.append({"kind": "numeric_mean_drift", **(numeric_detail or {})})


        if violations:
            per_col.append({"column": col, "violations": violations})

    summary = {
        "missing_columns": missing,
        "new_columns": added,
        "type_changes": type_changes,
        "row_count": {
            "baseline": base_rc,
            "new": new_rc,
            "ratio": rc_ratio,
            "ok": row_count_ok,
            "min_ratio": th["row_count_min_ratio"],
            "max_ratio": th["row_count_max_ratio"],
        },
        "per_column": per_col,
    }

    fail_reasons = []
    if len(added) > int(th["max_new_columns"]):
        fail_reasons.append("too_many_new_columns")
    if len(missing) > int(th["max_missing_columns"]):
        fail_reasons.append("too_many_missing_columns")
    if len(type_changes) > int(th["max_type_changes"]):
        fail_reasons.append("too_many_type_changes")
    if not row_count_ok:
        fail_reasons.append("row_count_out_of_bounds")
    if len(per_col) > 0:
        fail_reasons.append("column_drift")

    return {
        "ok": len(fail_reasons) == 0,
        "fail_reasons": fail_reasons,
        "summary": summary,
    }






