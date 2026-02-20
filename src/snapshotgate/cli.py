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




    check = sub.add_parser("check", help="Validate a file against a contract")
    check.add_argument("path", help="Input .csv or .jsonl")
    check.add_argument("--contract", required=True, help="Path to contract.json")
    check.add_argument("--out-dir", default="out", help="Output directory")
    check.add_argument("--max-rows", type=int, default=None, help="Profile only first N rows")

    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    try:
        if args.cmd == "learn":
            src = read_rows(args.path)
            prof = profile_rows(src, max_rows=args.max_rows)
            contract = make_contract(prof)
            write_json(contract, args.out)
            print(f"Wrote contract: {os.path.abspath(args.out)}")
            raise SystemExit(0)


