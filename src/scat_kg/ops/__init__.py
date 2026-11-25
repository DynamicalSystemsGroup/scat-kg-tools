"""The operations that write to a vault (R-4), and read its status. Each returns a `Result`."""

from scat_kg.ops.edges import record_edge, remove_edge
from scat_kg.ops.index import index
from scat_kg.ops.result import EdgeResult, Refusal, Result
from scat_kg.ops.status import StatusReport, StatusRow, read_status, set_status
from scat_kg.ops.stub import stub, stub_links

__all__ = [
    "EdgeResult",
    "Refusal",
    "Result",
    "StatusReport",
    "StatusRow",
    "index",
    "read_status",
    "record_edge",
    "remove_edge",
    "set_status",
    "stub",
    "stub_links",
]
