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



def read_jsonl_rows(path: str) -> RowSource:
    def gen() -> Iterator[dict[str, Any]]:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                if not isinstance(obj, dict):
                    continue
                yield obj

    return RowSource(name=os.path.basename(path), columns=[], rows=gen())



def read_rows(path: str) -> RowSource:
    p = path.lower()
    if p.endswith(".csv"):
        return read_csv_rows(path)
    if p.endswith(".jsonl"):
        return read_jsonl_rows(path)
    raise ValueError(f"Unsupported file type: {path}")



