import json
import os
import tempfile

from snapshotgate.contract import make_contract
from snapshotgate.io import RowSource
from snapshotgate.profiler import profile_rows
from snapshotgate.validate import validate





def test_smoke_contract_and_validate():
    base = RowSource(
        name="base.csv",
        columns=["id", "price", "status"],
        rows=[
            {"id": "1", "price": "10.0", "status": "active"},
            {"id": "2", "price": "11.0", "status": "active"},
            {"id": "3", "price": "12.0", "status": "draft"},
        ],
    )



