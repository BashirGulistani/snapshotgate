# SnapshotGate

SnapshotGate is a lightweight "data contract" gate for CSV and JSONL files.

It creates a baseline contract (schema + stats), then validates new files against it.
Useful for CI pipelines, ETL sanity checks, supplier feeds, and export drift detection.

## Install
pip install -e .


## Commands

### Create a contract
snapshotgate learn data.csv --out contract.json

### Validate a file against a contract
snapshotgate check data_new.csv --contract contract.json --out-dir out/

