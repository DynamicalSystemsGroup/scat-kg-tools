# STACK B (rdflib): rdflib store; rules in SHACL, run by pyshacl

Unit WP2-U3. All commands run from `research/toolchain/spike/` with the locked environment. Machine, library versions
and run counts are printed inside the `measure.py` output below. Numbers are one run of the command shown; rerun gives
the same shape, not identical digits.

## Thresholds (MISSION R-5, default thresholds) vs measured

Command (every number in the table):

```
uv run --locked python stacks/rdflib/measure.py
```

What is timed: one call of the check function at that scope on the 500-page synthetic vault (`gen_vault.py`, fixed
seed; generated fresh into a temp dir by `measure.py`), after `load()` and one untimed warm-up call per row. Each row
is `perf_counter` around the whole check call (for B this includes subgraph extraction, pyshacl and the report
mapping to messages). `load` (parse all 500 pages with `common.parse_vault`, build the stack's index or store) is
reported on its own row and is not in the check rows; the last line adds load + one check for a cold single invocation
(no cache is assumed). "hub" is the page with most links in + out (degree 7 in this vault: the generator makes
sparse, flat links, so neighborhoods are small); "typical" is the median-degree page. Sanity: every cell is asserted to
return 0 violations on the clean vault.

```
# measure.py: stack `rdflib`

- CPU: Intel(R) Core(TM) i9-10910 CPU @ 3.60GHz; cores: 20; RAM: 64 GiB
- OS: macOS-15.7.7-x86_64-i386-64bit-Mach-O
- Python: 3.14.3 (CPython)
- Libraries: rdflib=7.6.0, pyshacl=0.40.2, pydantic=2.14.4, python-frontmatter=1.3.0, pyyaml=6.0.4
- Vault: 500 pages, 560 links (gen_vault.py, seed fixed)
- Pages: hub = 'Affordance 003' (degree 7), typical = 'Attributes 075' (degree 2)
- Runs: 7 per local/neighborhood cell, 5 for full, plus 1 untimed warm-up each

| what is timed | median ms | min ms | max ms | n | threshold ms | verdict |
|---|---|---|---|---|---|---|
| load (parse + build, not a check) | 115.094 | 111.778 | 122.373 | 5 | - | - |
| local, hub | 1.583 | 1.565 | 1.708 | 7 | < 1000 | PASS |
| neighborhood, hub | 5.011 | 4.978 | 5.163 | 7 | < 2000 | PASS |
| local, typical | 2.018 | 2.000 | 2.093 | 7 | < 1000 | PASS |
| neighborhood, typical | 2.335 | 2.302 | 2.463 | 7 | < 2000 | PASS |
| full (500 pages) | 118.624 | 117.213 | 120.944 | 5 | < 5000 | PASS |

Cold single invocation (load + one check, medians added): local, hub = 116.7 ms; neighborhood, hub = 120.1 ms; full (500 pages) = 233.7 ms
Check outputs on the clean vault: 0 violations in every cell (asserted).
```

## How the rules are implemented

- The store is one rdflib `Graph` built from the parsed pages (`Store.add_page`): `sp:pageName`, `sp:pageType`,
  `sp:linksTo` (every link), `rdf:type` and one `FIELD/<key>` literal per plain field, and the TBox object property
  (for example `sp:addressesAffordance`) for each endpoint field. The vocabulary is documented in the `check.py`
  docstring; only the TBox properties come from `placeholder-tbox.ttl`.
- Shapes are generated from the TBox by `build_shapes` (29 lines), not hand-written Turtle: per class a `sh:NodeShape`
  with `sh:minCount 1` for each `sp:requiredField`; for an endpoint field the same property shape also has an `sh:node`
  requiring the target's `sp:pageType` to be the range class (`sh:hasValue`); one `Links` shape requires every
  `sp:linksTo` target to have an `sp:pageName` (a page exists). So the three rules are: `sh:minCount`,
  `sh:node`+`sh:hasValue`, `sh:node`+`sh:minCount` on the target.
- Local and neighborhood: `subgraph()` copies the checked pages' triples out of the store (neighborhood = page, its
  link targets that exist, its backlinks, found with `g.objects/subjects(sp:linksTo)`), then adds `sp:pageName` /
  `sp:pageType` stubs for link targets outside the set. Stubs carry no `rdf:type`, so no shape targets them and they
  are not themselves checked. Full: pyshacl validates the store directly.
- pyshacl is called with `inference="none"`, `advanced=False` (no SPARQL/JS rules needed).

## Mapping pyshacl's raw report to R-2 messages

pyshacl's report names a source shape IRI, a focus node IRI, a result path IRI, a value IRI and a generic constraint
component (see the raw reports below). It has no file name, no rule id, no fix. `to_violations()` (37 lines) turns
each top-level `sh:ValidationResult` into a message:

- file = `sp:pageName` of the focus node + `.md`;
- rule id from the constraint component and path: path `sp:linksTo` -> `broken-link`; `MinCountConstraintComponent` ->
  `missing-required-field`; `NodeConstraintComponent` with an existing target page -> `wrong-endpoint-class`;
- field = `rdfs:label` of the result path in the TBox (`sp:addressesAffordance` -> `affordance`) or the `FIELD/` key;
  for a broken link, the field is found by asking which store predicate links the focus to the missing value
  (else `(body)`);
- expected class = `rdfs:range` of the path in the TBox; found class = `sp:pageType` of the value;
- fix text = templates in Python, filled from the above, plus `difflib` closest page name and an example page of the
  right class (queried from the store);
- sub-results under `sh:detail` are dropped (the parent already reports them); an endpoint `sh:node` failure whose
  target page does not exist is dropped (the `broken-link` result covers it, otherwise one defect gives two messages).

Honest size: the mapping is about as large as the plain stack's rules. Counting what B needs beyond plain: graph build
(`add_page` ~18 lines), shape generation (29), subgraph extraction (14), report mapping (37). The SHACL layer does not
remove the message code; it moves the rule logic into shapes and adds a translation step. The message templates
(roughly 20 of the 37 lines) are identical in both stacks. Rule ids and fixes are not expressible in plain SHACL
(`sh:message` is a static string with no file or fix), so they would live in the mapping or as annotations on shapes
in any SHACL design. Not done: status strictness (R-3), `sh:severity`.

## Seeded defects: real output

Command:

```
uv run --locked python stacks/rdflib/defects.py
```

Each defect is made in a temp copy of `spike/vault` (the vault itself is never edited; baseline is 0 violations).
Output, unedited:

```
baseline spike/vault: 0 violations

=== defect 1 missing required field (Anonymity.md loses `description`)
--- raw engine report (pyshacl, unmodified)
Validation Report
Conforms: False
Results (1):
Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
	Severity: sh:Violation
	Source Shape: <https://example.org/scpt-spike/shape/Concern/description>
	Focus Node: <https://example.org/scpt-spike/page/Anonymity>
	Result Path: <https://example.org/scpt-spike/field#description>
	Message: Less than 1 values on <https://example.org/scpt-spike/page/Anonymity>-><https://example.org/scpt-spike/field#description>
--- final output (1 violation(s))
Anonymity.md: field "description" [missing-required-field] Concern pages require "description" (Less than 1 values on the path). Fix: add this line between the two --- lines at the top of Anonymity.md: description: <text>
--- same defect seen at narrower scopes on page 'Anonymity': local=1, neighborhood=1

=== defect 2 wrong endpoint class (Addresses.affordance -> a Concern)
--- raw engine report (pyshacl, unmodified)
Validation Report
Conforms: False
Results (1):
Constraint Violation in NodeConstraintComponent (http://www.w3.org/ns/shacl#NodeConstraintComponent):
	Severity: sh:Violation
	Source Shape: <https://example.org/scpt-spike/shape/Addresses/affordance>
	Focus Node: <https://example.org/scpt-spike/page/Anonymity%20addressed%20by%20Pseudonymous%20records>
	Value Node: <https://example.org/scpt-spike/page/Attribution>
	Result Path: <https://example.org/scpt-spike#addressesAffordance>
	Message: Value does not conform to Shape [ sh:property [ sh:hasValue <https://example.org/scpt-spike#Affordance> ; sh:path <https://example.org/scpt-spike#pageType> ] ]. See details for more information.
	Details:
		Constraint Violation in HasValueConstraintComponent (http://www.w3.org/ns/shacl#HasValueConstraintComponent):
			Severity: sh:Violation
			Source Shape: [ sh:hasValue <https://example.org/scpt-spike#Affordance> ; sh:path <https://example.org/scpt-spike#pageType> ]
			Focus Node: <https://example.org/scpt-spike/page/Attribution>
			Result Path: <https://example.org/scpt-spike#pageType>
			Message: Node <https://example.org/scpt-spike/page/Attribution>-><https://example.org/scpt-spike#pageType> does not contain a value in the set: ['<https://example.org/scpt-spike#Affordance>']
--- final output (1 violation(s))
Anonymity addressed by Pseudonymous records.md: field "affordance" [wrong-endpoint-class] Addresses.affordance links to [[Attribution]], which is a Concern; it must be an Affordance. Fix: in Anonymity addressed by Pseudonymous records.md change field affordance to the link of an Affordance page, for example affordance: "[[Locked dependencies]]".
--- same defect seen at narrower scopes on page 'Anonymity addressed by Pseudonymous records': local=1, neighborhood=1

=== defect 3 link to a missing page (Attribution.md body)
--- raw engine report (pyshacl, unmodified)
Validation Report
Conforms: False
Results (1):
Constraint Violation in NodeConstraintComponent (http://www.w3.org/ns/shacl#NodeConstraintComponent):
	Severity: sh:Violation
	Source Shape: <https://example.org/scpt-spike/shape/Links/linksTo>
	Focus Node: <https://example.org/scpt-spike/page/Attribution>
	Value Node: <https://example.org/scpt-spike/page/Nonexistent%20page>
	Result Path: <https://example.org/scpt-spike#linksTo>
	Message: Value does not conform to Shape [ sh:property [ sh:minCount Literal("1", datatype=xsd:integer) ; sh:path <https://example.org/scpt-spike#pageName> ] ]. See details for more information.
	Details:
		Constraint Violation in MinCountConstraintComponent (http://www.w3.org/ns/shacl#MinCountConstraintComponent):
			Severity: sh:Violation
			Source Shape: [ sh:minCount Literal("1", datatype=xsd:integer) ; sh:path <https://example.org/scpt-spike#pageName> ]
			Focus Node: <https://example.org/scpt-spike/page/Nonexistent%20page>
			Result Path: <https://example.org/scpt-spike#pageName>
			Message: Less than 1 values on <https://example.org/scpt-spike/page/Nonexistent%20page>-><https://example.org/scpt-spike#pageName>
--- final output (1 violation(s))
Attribution.md: field "(body)" [broken-link] link [[Nonexistent page]] points to no page. Fix: create the file "Nonexistent page.md" starting with these lines: --- / type: <one of StakeholderGroup, Concern, Affordance, Technology> / name: Nonexistent page / status: stub / ---
--- same defect seen at narrower scopes on page 'Attribution': local=1, neighborhood=1
```

The `--- raw engine report` blocks above are pyshacl's own `validate()` text, unmodified.

The last line of each block shows the same defect found when only the defective page is checked at local scope
and at neighborhood scope.

## Judgement against R-2 (file; field or link; rule id; fix a literal reader can apply)

| defect | file | field/link | rule id | exact fix | verdict |
|---|---|---|---|---|---|
| 1 missing field | yes | yes (`description`) | yes | yes: names the line and where it goes; the value is `<text>` | meets R-2; same text as stack C except the parenthesis, which quotes pyshacl's "Less than 1 values" |
| 2 wrong endpoint class | yes | yes | yes | partly: literal example link, chosen alphabetically | meets R-2 for a literal reader; the example is a guess |
| 3 missing page | yes | the link `[[Nonexistent page]]` is named; field `(body)` | yes | partly: retarget or create file; `type:` is a placeholder for a body link | meets R-2 except the class of the new page |

The raw pyshacl reports alone do NOT meet R-2: no file name (only a page IRI), no rule id (only a SHACL constraint
component name), no fix. Defect 3's raw report also gives the offending link only as a percent-encoded IRI and a
nested detail about `sp:pageName`.

Rule ids here are the spike's own (`missing-required-field`, `wrong-endpoint-class`, `broken-link`), not final ids.

## Reproduce

```
cd research/toolchain/spike
uv run --locked python stacks/rdflib/check.py vault        # baseline: ok: 0 violations (22 pages)
uv run --locked python stacks/rdflib/defects.py             # the three defect outputs
uv run --locked python stacks/rdflib/measure.py             # the timing table
```

Baseline output:

```
ok: 0 violations (22 pages)
```

## Not covered (spike scope)

Status strictness (R-3: all missing fields are errors here), pages without a `type` or with an unknown `type` (silently
skipped), an endpoint value that is not a `[[link]]` (reported as a missing field), line numbers, R-13, OKF.
