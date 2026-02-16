from __future__ import annotations

import math
import re
from datetime import datetime
from typing import Any


_ws = re.compile(r"\s+")


def norm_str(x: Any) -> str:
    if x is None:
        return ""
    s = str(x).strip()
    s = _ws.sub(" ", s)
    return s


def is_empty(x: Any) -> bool:
    if x is None:
        return True
    if isinstance(x, str):
        return norm_str(x) == ""
    if isinstance(x, float) and math.isnan(x):
        return True
    return False


def try_float(x: Any) -> float | None:
    if x is None:
        return None
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        try:
            v = float(x)
            if math.isnan(v) or math.isinf(v):
                return None
            return v
        except Exception:
            return None
    s = norm_str(x)
    if s == "":
        return None
    s2 = s.replace(",", "")
    try:
        v = float(s2)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except Exception:
        return None



