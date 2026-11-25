"""The machine interface's schema as a validator, for the operation tests."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA = json.loads(
    (Path(__file__).parents[2] / "contracts" / "machine-interface.schema.json").read_text("utf-8")
)
VALIDATOR = Draft202012Validator(SCHEMA)
