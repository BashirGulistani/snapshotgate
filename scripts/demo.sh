#!/usr/bin/env bash
set -euo pipefail

rm -rf out_ok out_fail || true

echo "Learning baseline contract..."
snapshotgate learn examples/sample_data/baseline.csv --out examples/contracts/contract.template.json

echo "Checking new_ok (should pass)..."
snapshotgate check examples/sample_data/new_ok.csv --contract examples/contracts/contract.template.json --out-dir out_ok

echo "Checking new_fail (should fail)..."
set +e
snapshotgate check examples/sample_data/new_fail.csv --contract examples/contracts/contract.template.json --out-dir out_fail
code=$?
set -e

echo ""
echo "Exit code (expected non-zero for fail): $code"
echo "Open reports:"
echo "  out_ok/report.html"
echo "  out_fail/report.html"
