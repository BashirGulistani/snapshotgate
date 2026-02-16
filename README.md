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

### JSONL supported too
snapshotgate learn events.jsonl --out contract.json
snapshotgate check events_new.jsonl --contract contract.json --out-dir out/

## What it checks

- Missing / new columns
- Type changes (string/number/bool/date-ish)
- Null-rate spikes
- Numeric drift (mean/std shift)
- Cardinality drift (unique counts)
- Top-value drift for categorical columns
- Row count anomalies (optional thresholds)

## Exit codes
- 0: pass
- 1: violations found
- 2: errors / invalid input

## License
MIT
