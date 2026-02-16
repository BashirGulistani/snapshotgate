# SnapshotGate

SnapshotGate is a lightweight "data contract" gate for CSV and JSONL files.

It creates a baseline contract (schema + stats), then validates new files against it.
Useful for CI pipelines, ETL sanity checks, supplier feeds, and export drift detection.

## Install
pip install -e .


