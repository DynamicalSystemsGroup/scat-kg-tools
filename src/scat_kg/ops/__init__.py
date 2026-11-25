"""The operations that write to a vault (R-4), and read its status. Each returns a `Result`."""

from scat_kg.ops.index import index
from scat_kg.ops.result import Refusal, Result
from scat_kg.ops.status import StatusReport, StatusRow, read_status, set_status
from scat_kg.ops.stub import stub, stub_links, stub_pair

__all__ = [
    "Refusal",
    "Result",
    "StatusReport",
    "StatusRow",
    "index",
    "read_status",
    "set_status",
    "stub",
    "stub_links",
    "stub_pair",
]
