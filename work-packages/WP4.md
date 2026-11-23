# WP4 — Scope of work: Ontology and page contracts

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md`: G1, G2, G3, R-1, R-2, R-3, R-13, the platform constraint, and deliverable D-1. |
| **Branch** | Each unit works on `wp4/u<k>`, branched off `dev` and merged back into `dev` (ORG.md). |
| **Inputs** | `research/ontology/readout.md`, `research/toolchain/readout.md` and `measurements.md`, `research/facilitation/readout.md`, and the rulings in `decisions/log.md` D-028 |

## Purpose

Fix what a conformant SCAT vault is, before any production code exists. The output has three parts:
- **the TBox:** the classes, relations, fields and status values;
- **the page contracts:** how each page type looks on disk in an Obsidian vault;
- **the rule catalogue:** what is checked, at what severity, and what each message tells the user to do.

These must be clear enough for WP5 to implement without guessing, and for a person to hand-write a conformant page.

## Goals

- **WP4-G1. TBox** in Turtle. It follows the composition D-028 accepted:
  - a SKOS spine, with authored SCAT IRIs, adopted definitions and `closeMatch` anchors;
  - the conflict relation D1;
  - `prov:wasDerivedFrom` from coded to raw records;
  - a status property, adopted or authored, as D-028 allows.

  It states everything the checks need from it, including type slugs, descriptions, required and optional fields,
  status values and link rules, so that R-13 can hold the tools to it.
- **WP4-G2. Page contracts.** For each page type (the four classes, the three relations, raw and coded scenarios, raw
  and coded architectures, and class pages), the contract sets out:
  - the frontmatter keys;
  - how links are written and which links are typed edges;
  - how a page is named and addressed, including the rule for names that collide or differ only by case;
  - which links entail which pages, so the stub operation can create them with the right type (body links
    included);
  - how the conflict relation D1 is written (a typed link, or a page), decided here;
  - where the vault's stakeholder-group cap is set (the instance configuration), and its format;
  - what a class page and its index table look like;
  - how raw records link to or embed their coded pages.
- **WP4-G3. Rule catalogue.** Every rule has an id, a severity, a trigger and a message with an exact fix, covering
  the R-1 error classes, R-3's status behaviour, the D3 conflict warning, the unlinked-mention warning and the
  raw-to-coded warning. It settles the four decisions that `research/toolchain/measurements.md` ("What it takes to
  make each fix exact") found exact fixes depend on:
  - the missing-field fix;
  - the tie-break for a wrong relation endpoint;
  - the stub type for a dangling link;
  - the fix for a missing link type.

  On the last, the ACE has ruled (log D-029): no new TBox axiom. The fix names the exact field to fill and may
  suggest candidates, and the rule records why the choice stays with the author.
- **WP4-G4.** A minimal valid example of each page type, including examples that show capabilities 1–3 from D-028: a
  concern shared by two groups, two concerns in conflict, and groups that share one concern while differing on others.

## Non-goals

- Implementation (WP5). The template and case study (WP6). The docs guides (WP7).
- Any element beyond `MISSION.md` G1 and D1 without a written trade-off.
- Re-opening the toolchain or composition rulings in D-028, except through an escalation to the ACE with evidence.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP4-D1 | `ontology/scat.ttl`: the TBox (mission deliverable D-1) | WP4-G1 |
| WP4-D2 | `contracts/page-contracts.md` | WP4-G2 |
| WP4-D3 | `contracts/rule-catalogue.md` | WP4-G3 |
| WP4-D4 | `contracts/examples/`: one valid page per page type, plus the capability examples | WP4-G4 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP4-R1 | `scat.ttl` parses as Turtle. | `uv run --with rdflib python -c "import rdflib; rdflib.Graph().parse('ontology/scat.ttl')"`, with output pasted in the PR; no dependency change |
| WP4-R2 | Every SCAT term has a `skos:definition` and either a source anchor or an "authored" note with its reason. Definitions not checked against a primary source carry the marker `scat:verification "unverified"`, or an equivalent the TBox defines. | A script, kept in the scratchpad with its output pasted in the PR, that lists the terms missing a definition, a source or authored note, or a verification status |
| WP4-R3 | The TBox states, for each page type, its slug, description, required and optional fields, status values and link rules. A tool could generate models from it, or test against it, without consulting any other file. | The reviewer derives, for two page types, the field list from the TBox alone and compares it with the contracts |
| WP4-R4 | Every rule has an id, a severity, a trigger and a message template. The fix is exact (a command, or a field and value), or the rule records why it cannot be. Rules cover every R-1 class, R-3's status behaviour, D3, and both warnings. | A checklist over the catalogue |
| WP4-R5 | The page contracts and the TBox agree: every contract field and link is in the TBox, and every TBox field appears in a contract. This includes D1 and the cap's configuration. | The reviewer's cross-check |
| WP4-R6 | The naming rule rules out collisions across case-sensitive and case-insensitive file systems, and characters unsafe on macOS, Linux or Windows. | Inspection against the platform constraint |
| WP4-R7 | Each example page conforms to its contract, and the capability examples show capabilities 1–3. | The reviewer checks each example against its contract |
| WP4-R8 | **Cold-write test.** A fresh Haiku worker, given only `page-contracts.md` and `rule-catalogue.md` (no TBox, no examples), writes a valid coded scenario, a valid coded architecture, and the pages they entail, in a domain of its own. A reviewer finds them conformant, or each defect traces to an unclear contract, which is then fixed, and a fresh Haiku worker reruns the test. | The worker's pages and the reviewer's report, in the PR description, not committed |

## Definition of good

A person can read the contracts and hand-write a conformant page on the first try. WP5 can implement every rule
without asking a question. The ontology is small enough to hold in your head.

## Definition of good enough

WP4-R1 to WP4-R8 are met.

## Blast radius

`ontology/**` and `contracts/**` only. Scripts and cold-write pages live in the scratchpad, and their output goes in
the PR description.

## Agent's defaults

- Paths: `ontology/` and `contracts/` at the root of `scat-kg-tools`. WP5 decides how the package ships them.
- Rule ids are prefixed `SCAT-`.
