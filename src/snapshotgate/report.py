from __future__ import annotations

import json
import os
from typing import Any


def _load_template() -> str:
    here = os.path.dirname(__file__)
    path = os.path.join(here, "templates", "report.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_report_html(contract: dict[str, Any], new_profile: dict[str, Any], validation: dict[str, Any], out_path: str) -> None:
    tpl = _load_template()
    payload = {
        "contract": contract,
        "new_profile": new_profile,
        "validation": validation,
    }
    js = json.dumps(payload, ensure_ascii=False)
    html = tpl.replace("{{__DATA__}}", js)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
