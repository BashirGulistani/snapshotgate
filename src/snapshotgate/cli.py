from __future__ import annotations

import argparse
import os
import sys

from .contract import make_contract
from .io import ensure_out_dir, read_rows, write_json
from .profiler import profile_rows
from .report import write_report_html
from .validate import validate




def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="snapshotgate", add_help=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    learn = sub.add_parser("learn", help="Create a baseline contract from a file")
    learn.add_argument("path", help="Input .csv or .jsonl")
    learn.add_argument("--out", required=True, help="Contract output path (json)")
    learn.add_argument("--max-rows", type=int, default=None, help="Profile only first N rows")





