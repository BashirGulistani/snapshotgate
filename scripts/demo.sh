#!/usr/bin/env bash
set -euo pipefail

rm -rf out_ok out_fail || true

echo "Learning baseline contract..."
snapshotgate learn examples/sample_data/baseline.csv --out examples/contracts/contract.template.json
