"""The index operation: the Base files of the generated index pages (page contracts 9).

TODO(WP16-U7): rebuilt for the row model; the class pages this module wrote are gone.
"""

from pathlib import Path

from scat_kg.ops.result import Result, not_built


def index(*, root: str | Path = ".") -> Result:
    """TODO(WP16-U7): write `index/<type>.base` for each type that has none."""
    return not_built("index")
