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

    def add(self, v: Any) -> None:
        self.count += 1
        if is_empty(v):
            self.nulls += 1
            return

        sv = norm_str(v)
        fb = try_bool(v)
        fd = try_dateish(v)
        ff = try_float(v)

        if ff is not None:
            self.num_count += 1
            delta = ff - self.num_mean
            self.num_mean += delta / self.num_count
            delta2 = ff - self.num_mean
            self.num_m2 += delta * delta2
        elif fb is not None:
            pass
        elif fd is not None:
            pass
        else:
            pass






