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


    def finalize(self, uniques: set[str], top_map: dict[str, int], type_votes: dict[str, int]) -> dict[str, Any]:
        inferred = "string"
        if type_votes:
            inferred = max(type_votes.items(), key=lambda kv: kv[1])[0]

        var = safe_div(self.num_m2, (self.num_count - 1)) if self.num_count > 1 else 0.0
        std = var ** 0.5

        top = sorted(top_map.items(), key=lambda kv: kv[1], reverse=True)[:12]
        return {
            "name": self.name,
            "inferred_type": inferred,
            "count": self.count,
            "nulls": self.nulls,
            "null_rate": safe_div(self.nulls, self.count),
            "unique_approx": len(uniques),
            "top_values": top,
            "numeric": {
                "count": self.num_count,
                "mean": self.num_mean if self.num_count else 0.0,
                "std": std if self.num_count else 0.0,
            },
        }


def infer_type_vote(v: Any) -> str:
    if is_empty(v):
        return "empty"
    if try_float(v) is not None:
        return "number"
    if try_bool(v) is not None:
        return "bool"
    if try_dateish(v) is not None:
        return "date"
    return "string"


def profile_rows(src: RowSource, max_rows: int | None = None) -> dict[str, Any]:
    colnames: set[str] = set(src.columns)

    profiles: dict[str, ColProfile] = {}
    uniques: dict[str, set[str]] = {}
    top_map: dict[str, dict[str, int]] = {}
    type_votes: dict[str, dict[str, int]] = {}

    row_count = 0
    for row in src.rows:
        row_count += 1
        if max_rows is not None and row_count > max_rows:
            break

        for k in row.keys():
            colnames.add(norm_str(k))

        for col in colnames:
            if col not in profiles:
                profiles[col] = ColProfile(
                    name=col, inferred_type="string",
                    count=0, nulls=0, unique_approx=0,
                    top_values=[], num_count=0, num_mean=0.0, num_m2=0.0
                )
                uniques[col] = set()
                top_map[col] = {}
                type_votes[col] = {}

            v = row.get(col)
            profiles[col].add(v)

            if not is_empty(v):
                sv = norm_str(v)
                if len(uniques[col]) < 5000: 
                    uniques[col].add(sv)
                if len(sv) <= 120:
                    top_map[col][sv] = top_map[col].get(sv, 0) + 1

                t = infer_type_vote(v)
                if t != "empty":
                    type_votes[col][t] = type_votes[col].get(t, 0) + 1

    cols_sorted = sorted(list(colnames))
    out_cols = []
    for c in cols_sorted:
        out_cols.append(profiles[c].finalize(uniques[c], top_map[c], type_votes[c]))

    return {
        "source": src.name,
        "row_count": row_count,
        "columns": cols_sorted,
        "profiles": out_cols,
    }



