from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Thresholds:
    max_new_columns: int = 0
    max_missing_columns: int = 0
    max_type_changes: int = 0
    max_null_rate_increase: float = 0.10
