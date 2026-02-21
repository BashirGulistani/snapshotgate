
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






