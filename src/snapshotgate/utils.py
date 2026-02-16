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



