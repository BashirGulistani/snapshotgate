from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass
from typing import Any, Iterable, Iterator

from .utils import norm_str


@dataclass(frozen=True)
class RowSource:
    name: str
    columns: list[str]
    rows: Iterable[dict[str, Any]]



def ensure_out_dir(out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def read_csv_rows(path: str) -> RowSource:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = [norm_str(c) for c in (reader.fieldnames or [])]

        def gen() -> Iterator[dict[str, Any]]:
            for r in reader:
                row = {}
                for k, v in r.items():
                    row[norm_str(k)] = v
                yield row

        return RowSource(name=os.path.basename(path), columns=cols, rows=gen())






