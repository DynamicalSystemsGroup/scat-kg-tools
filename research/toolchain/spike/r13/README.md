# R-13: one source for the schema

`models.py` builds the pydantic models from `../placeholder-tbox.ttl` at import time (`pydantic.create_model`).
No class, field or status is written by hand, so a TBox change shows up in the models with no second edit.
`test_r13.py` checks the models against an independent SPARQL read of the TBox.

Why generate-at-import rather than hand-written models plus an equality test: there is no second copy to keep
equal, so no generated file to forget to regenerate. The cost is that the models are not static, so editors
and type checkers cannot see the fields.

## Run

```
uv run --locked pytest r13                 # all tests, including the automated drift demo
uv run --locked python r13/models.py       # validate the 22-page mini-vault through the models
```

## One-line manual drift demo (temporary copy; the real TBox is never touched)

```
sed 's/sp:optionalField "category" ./sp:optionalField "category", "severity" ./' placeholder-tbox.ttl > /tmp/t.ttl && uv run --locked python -c "import sys; sys.path.insert(0,'r13'); import models; print(sorted(models.MODELS['Concern'].model_fields)); print(sorted(models.load('/tmp/t.ttl')[0]['Concern'].model_fields))"
```

Run from `research/toolchain/spike`. The first line printed has no `severity`; the second does.

## What the TBox cannot express (the models need it)

- `type`, `status`, and (for the three relation classes) `name` are not in the TBox's field lists; the models make all three required on every class by convention. The test compares TBox fields minus these.
- Field value types: every field is a string. The TBox has no datatypes (`homepage` is not a URL, `metric` not a number).
- A link field is recognised only because an ObjectProperty's `rdfs:label` equals the field name (domain = relation class).
  That is a naming convention, not OWL semantics.
- Extra keys are rejected (`extra="forbid"`): a modelling choice with no TBox term.
- Link syntax (`"[[...]]"`) is a page-format rule from the spike README, hardcoded in `models.py`.
- Status order is read from `sp:rank`; the models only use it for listing, no transition rules.
