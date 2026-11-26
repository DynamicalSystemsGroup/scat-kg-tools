"""The operations that write to a vault (R-4), and read its status. Each returns a `Result`."""

from scat_kg.ops.edges import record_edge, remove_edge
from scat_kg.ops.index import index
from scat_kg.ops.merge import MergeResult, merge
from scat_kg.ops.result import EdgeResult, Refusal, Result
from scat_kg.ops.split import SplitPlan, split_plan
from scat_kg.ops.status import StatusReport, StatusRow, read_status, set_status
from scat_kg.ops.stub import stub, stub_links

__all__ = [
    "EdgeResult",
    "MergeResult",
    "Refusal",
    "Result",
    "SplitPlan",
    "StatusReport",
    "StatusRow",
    "index",
    "merge",
    "read_status",
    "record_edge",
    "remove_edge",
    "set_status",
    "split_plan",
    "stub",
    "stub_links",
]
