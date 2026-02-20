from __future__ import annotations

import argparse
import os
import sys

from .contract import make_contract
from .io import ensure_out_dir, read_rows, write_json
from .profiler import profile_rows
from .report import write_report_html
from .validate import validate




