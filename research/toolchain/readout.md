# WP2-D3: toolchain readout

Evidence and rerun commands are in `measurements.md` (sections named below). Everything was rerun on one
machine: an Intel i9-10910, 20 cores, macOS 15.7.7, Python 3.14.3.

## Recommendation: stack C (pydantic models plus plain Python)

What decided it:

- **R-5 is met with room by all three stacks.** Full-vault medians on 500 pages: C 0.059 s, A 0.133 s, B 0.495 s
  (limit 5 s). The one failure is B's `sh:sparql` variant: 12.6 s full vault. Speed does not separate A, B and C
  (Timings); it does exclude B's `sh:sparql` shapes.
- **Messages do not separate them either.** In the stack x defect table, all 12 cells name file, field and rule id.
  Only the dangling link has an exact fix, in all three stacks. The other fixes are candidates the author confirms,
  or have a placeholder (Stack x defect). B's wording is the most pasteable and A's the least; the difference is
  message text, which any stack can copy. What the fixes would need is in `measurements.md` (WP2-R8).
- **So simplicity decides.** C has no graph store and no second rule language: rules are pydantic models and
  Python, which a contributor reads without knowing SPARQL or SHACL. A and B each add an RDF layer and a rule
  language; B adds pyshacl and its own message layer on top of SHACL reports.
- **C did something A and B did not in one spot check.** With a bad `status` and a bad `type`, C gave two clear
  messages (`SCAT-FM-STATUS`, `SCAT-FM-TYPE`). A gave none for status and four misleading endpoint errors for the
  type. B was not run (its README says it is not implemented).

C is not smaller: `checks.py` and `models.py` total 487 lines, against 249 for A's `core.py` and 335 for B's
`check.py`. I chose it for what a contributor must learn, not for line count.

## OKF verdict: not as the format between vault and graph

Pinned commit `527e81aff55992be21507e97004286789126f88c` (spec v0.3). I ran its `validate.py` and graph builder
(PyYAML only; the reference agent was not installed: it needs google-adk, BigQuery and credentials). Pasted output
is in `measurements.md` (OKF trial):

- `validate.py` on the vault: "20 files checked: 0 errors, 14 warnings, 18 info. The bundle is conformant."
- On the four seeded defects it reported nothing new for three, and one changed info line for the fourth: 0 of 4
  detected.
- Graph builder: `edges: 0`. The vault has 47 wikilinks, 41 of them typed edges in frontmatter. OKF's spec
  (section 6.1) says wikilinks are not links.
- Its `status` vocabulary (`draft|stable|deprecated`) clashes with ours: `done` and `stub` draw 14 warnings.

Adopting it would mean rewriting links as markdown links and renaming statuses, and the checker would still be
ours. It adds nothing we lack.

## R-13 result

The mechanism works for C. `pytest r13 -q`: 5 passed. The demo adds `scat:raw` to CodedScenario's required links
in a scratch TBox and the equality test fails, naming the class and the difference. The test compares classes, link
properties, ranges, domains and required link sets. It cannot compare type slugs, `description` or status values,
because the placeholder TBox does not state them; the real TBox (D-1) would have to, or a generator would replace
the test. I ran no equivalent for A's SPARQL or B's SHACL.

## Platform-specific items in the recommended stack (WP2-R9)

Governance constraint: macOS supported; nothing that puts Linux or Windows at risk.

- **Paths:** `pathlib.Path` and a flat directory of `<stem>.md`; no hard-coded separators. Isolated in `Vault`.
- **Line endings:** files are read with `read_text(encoding="utf-8")`, which normalises CRLF. A CRLF copy of the
  mini-vault checked with C gave 0 violations (ad hoc check). C only reads, so writing is not exercised.
- **Shells:** none used by the checks. Only `bench.py` shells out, to `sysctl` on macOS for the CPU name; it is a
  spike tool, guarded by `sys.platform`, and does not go into the package.
- **Tools:** uv and CPython only. PyYAML uses libyaml when present and falls back to pure Python; pydantic ships
  compiled wheels for macOS, Linux and Windows.
- **File names:** macOS file systems are usually case-insensitive and Linux ones are not, so stems that differ only
  by case would collide on one and not the other. The spike does not test it; the page contracts should settle it.

Nothing in C is unavoidably platform-specific. No Linux or Windows run was made; this list comes from reading the
code and the CRLF check.

## Dependencies beyond the pre-approved list

None for stack C: it uses pydantic and PyYAML (python-frontmatter is not needed). `ruff` is a dev dependency of
the spike project, not of C.

## Weaknesses and what was not measured

- Benches ran on a 20-core desktop, not a typical laptop. R-5 is stated for a laptop; the headroom (8x or more)
  is the evidence, not proof.
- The spike's rule coverage is partial (six to ten rules per stack) and rests on a placeholder TBox. It does not
  decide the TBox or the rule catalogue.
- Rule coverage differs by stack, so timings compare stacks doing different amounts of work; page scopes load
  different amounts too.
- C's models are hand-written and held equal to the TBox by a test that cannot see slugs, `description` or
  statuses. That is a standing cost for C; A and B may carry it differently, and I did not measure it.
- Three of four defects have no exact fix without a project decision (WP2-R8). C's fixes carry a placeholder or a
  choice.
- C reports no line numbers (B does, for link fields).
- Bad `status` and `type` values were tested in one spot check only.
- Seven repeats (three for `sh:sparql`), warm OS cache, one machine; no variance across machines.
