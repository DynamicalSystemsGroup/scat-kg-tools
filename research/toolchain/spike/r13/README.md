# R-13 mechanism (WP2-G5, WP2-R5): models held equal to the TBox by a test

Chosen mechanism: the stack C pydantic models (`stacks/c/models.py`) are hand-written but **held equal** to
`placeholder-tbox.ttl` by a pytest equality test. The TBox is authoritative; a TBox change that the models do
not follow fails the test, with a message naming the difference and the model edit to make.

Compared (`equality.py`): the set of page classes; the set of link properties (TBox ObjectProperties vs link
fields of the models); each property's `rdfs:range` and `rdfs:domain`; each class's `scat:requiresLink` set
vs the model's `REQUIRED_LINKS`.

Not comparable, because the placeholder TBox does not state them: type slugs (`scenario-coded`), `description`,
status values, which classes carry which optional link fields beyond a stated domain. These live in the models
only; closing that gap needs the real TBox (D-1) to state them, or a generator instead of an equality test.

All commands run from the repository root.

```
# the equality test on the unchanged TBox, plus four mutation tests (each edits an in-memory scratch copy)
uv run --directory research/toolchain/spike python -m pytest r13 -q
# the demonstration: same test on the TBox, then on a scratch copy with a changed TBox (fails, names why)
uv run --directory research/toolchain/spike python -m r13.demo
# by hand: run the test against any scratch TBox
SCAT_TBOX=/path/to/scratch.ttl uv run --directory research/toolchain/spike python -m pytest r13/test_equality.py::test_models_equal_tbox -q
```

The real TBox is never written; the demo and the mutation tests use temporary copies.
