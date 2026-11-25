"""The stub operations: pages that a link or a row end entails (page contracts 6).

TODO(WP16-U7): rebuilt for the row model; the raw and coded pages and the relation pages they wrote are gone.
"""

from pathlib import Path

from scat_kg.ops.result import Result, not_built


def stub(name: str, type: str | None = None, *, root: str | Path = ".") -> Result:  # TODO(WP16-U7)
    return not_built("stub")


def stub_links(page: str | None = None, *, root: str | Path = ".") -> Result:  # TODO(WP16-U7)
    return not_built("stub-links")


def stub_pair(
    relation: str, endpoint_a: str, endpoint_b: str, *, root: str | Path = "."
) -> Result:  # TODO(WP16-U7)
    return not_built("stub-pair")
