# Contributing to SnapshotGate

Thanks for contributing.

## Dev setup

1. Create venv
   - python -m venv .venv
   - source .venv/bin/activate

2. Install
   - pip install -e .



3. Run tests
   - python -m pip install pytest
   - pytest -q

## What to contribute

- More robust type inference
- Better drift checks (percentiles, min/max, time-series)
- Performance improvements for very large CSV/JSONL
- Better HTML report UX (sorting, grouping, filters)

## Style

- Keep dependencies minimal
- Avoid heavy frameworks unless clearly necessary
- Favor readability over cleverness

## PR checklist

- Tests added/updated
- README updated if behavior changes
- Keep changes small and focused
