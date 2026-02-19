from __future__ import annotations

import json
import os
from typing import Any


def _load_template() -> str:
    here = os.path.dirname(__file__)
    path = os.path.join(here, "templates", "report.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


