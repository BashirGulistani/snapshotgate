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

def try_bool(x: Any) -> bool | None:
    if x is None:
        return None
    if isinstance(x, bool):
        return x
    s = norm_str(x).lower()
    if s in ("true", "t", "1", "yes", "y"):
        return True
    if s in ("false", "f", "0", "no", "n"):
        return False
    return None


def try_dateish(x: Any) -> str | None:
    """
    Returns ISO date string if parseable, else None.
    (We keep it lightweight: common formats only.)
    """
    if x is None:
        return None
    if isinstance(x, datetime):
        return x.isoformat()
    s = norm_str(x)
    if not s:
        return None

    fmts = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]
    for f in fmts:
        try:
            dt = datetime.strptime(s, f)
            return dt.isoformat()
        except Exception:
            pass
    return None


def safe_div(a: float, b: float) -> float:
    if b == 0:
        return 0.0
    return a / b

