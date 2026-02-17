from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .io import RowSource
from .utils import is_empty, norm_str, safe_div, try_bool, try_dateish, try_float



@dataclass
class ColProfile:
    name: str
    inferred_type: str  
    count: int
    nulls: int
    unique_approx: int
    top_values: list[tuple[str, int]]  
    num_count: int
    num_mean: float
    num_m2: float  

