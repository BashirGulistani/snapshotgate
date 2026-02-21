
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class Severity:

    missing_columns: str = "fail"   
    new_columns: str = "warn"
    type_changes: str = "fail"
    row_count: str = "warn"
    column_drift: str = "fail"



@dataclass(frozen=True)
class GateThresholds:

    max_new_columns: int = 0
    max_missing_columns: int = 0
    max_type_changes: int = 0

    row_count_min_ratio: float = 0.70
    row_count_max_ratio: float = 1.40

    max_null_rate_increase: float = 0.10     
    max_unique_rate_change: float = 0.50        
    max_top_value_jaccard_drop: float = 0.35    
    max_numeric_mean_z: float = 4.0             

    ignore_columns: list[str] = field(default_factory=list)



@dataclass(frozen=True)
class ColumnOverride:

    ignore: bool = False

    max_null_rate_increase: float | None = None
    max_unique_rate_change: float | None = None
    max_top_value_jaccard_drop: float | None = None
    max_numeric_mean_z: float | None = None

    expect_type: str | None = None 


def _merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:

    out = dict(base)
    for k, v in patch.items():
        out[k] = v
    return out


def presets() -> dict[str, dict[str, Any]]:

    strict = asdict(GateThresholds(
        max_new_columns=0,
        max_missing_columns=0,
        max_type_changes=0,
        row_count_min_ratio=0.85,
        row_count_max_ratio=1.15,
        max_null_rate_increase=0.05,
        max_unique_rate_change=0.25,
        max_top_value_jaccard_drop=0.20,
        max_numeric_mean_z=3.0,
    ))


    default = asdict(GateThresholds())

    lenient = asdict(GateThresholds(
        max_new_columns=5,
        max_missing_columns=2,
        max_type_changes=2,
        row_count_min_ratio=0.50,
        row_count_max_ratio=2.00,
        max_null_rate_increase=0.20,
        max_unique_rate_change=1.00,
        max_top_value_jaccard_drop=0.55,
        max_numeric_mean_z=6.0,
    ))

    return {"strict": strict, "default": default, "lenient": lenient}


def default_thresholds(profile: str = "default") -> dict[str, Any]:
    p = presets()
    if profile not in p:
        profile = "default"
    return p[profile]


def default_severity() -> dict[str, Any]:
    return asdict(Severity())



def make_contract(
    profile: dict[str, Any],
    thresholds: dict[str, Any] | None = None,
    *,
    threshold_profile: str = "default",
    severity: dict[str, Any] | None = None,
    column_overrides: dict[str, dict[str, Any]] | None = None,
    notes: str | None = None,
) -> dict[str, Any]:

    base_th = default_thresholds(threshold_profile)
    th = _merge(base_th, thresholds or {})
    sev = _merge(default_severity(), severity or {})

    col_ov: dict[str, Any] = {}
    if column_overrides:
        for col, ov in column_overrides.items():
            if not isinstance(ov, dict):
                continue
            allowed = set(asdict(ColumnOverride()).keys())
            clean = {k: v for k, v in ov.items() if k in allowed}
            col_ov[col] = clean

    return {
        "version": 2,
        "baseline": profile,
        "threshold_profile": threshold_profile,
        "thresholds": th,
        "severity": sev,
        "column_overrides": col_ov,
        "notes": notes or "",
    }








