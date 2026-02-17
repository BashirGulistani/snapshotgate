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







