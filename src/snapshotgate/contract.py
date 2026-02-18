from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Thresholds:
    max_new_columns: int = 0
    max_missing_columns: int = 0
    max_type_changes: int = 0
    max_null_rate_increase: float = 0.10
    max_unique_rate_change: float = 0.50
    max_top_value_jaccard_drop: float = 0.35
    max_numeric_mean_z: float = 4.0  

    row_count_min_ratio: float = 0.70
    row_count_max_ratio: float = 1.40


def default_thresholds() -> dict[str, Any]:
    return Thresholds().__dict__


