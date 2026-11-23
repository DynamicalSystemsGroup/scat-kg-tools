# WP2 — Scope of work: Toolchain spike

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md` (G8, R-5, R-13, deliverable D-5). |
| **Branch** | `wp2/toolchain-spike`, units off it, merged into `dev` |

## Purpose

Choose the toolchain by measurement, before implementation is locked in. The candidates are:
- the parser for markdown with YAML frontmatter and wikilinks;
- the graph store and query engine (oxigraph, rdflib);
- the rule language (SHACL through pyshacl, SPARQL queries in oxigraph, pydantic and plain Python);
- the single-source schema mechanism (R-13);
- Open Knowledge Format (OKF) as the format between the vault and the graph.

## Goals

- G1. Build a throwaway mini-vault of about 20 pages, using the seven SCPT classes as `MISSION.md` G1 names them (a
  placeholder schema; WP1 decides the real terms). Also build a generator for a synthetic 500-page vault.
- G2. For each candidate stack, measure local, neighborhood and full checks against R-5's thresholds (< 1 s, < 2 s,
  < 5 s on the 500-page vault), on this machine.
- G3. For each rule-language option, produce the actual error output for three seeded defects (missing required field,
  relation endpoint of the wrong class, link to a missing page). Judge it against R-2: file, field, rule id, and an
  exact fix.
- G4. Try OKF hands-on (<https://github.com/open-knowledge-format/open-knowledge-format>): install it, run it on the
  mini-vault, and give a verdict on whether it can be the format between vault and graph.
- G5. Demonstrate one R-13 mechanism: the TBox as the source, with pydantic models generated from it or tested equal
  to it.
- G6. Recommend a toolchain in a readout of at most two pages.

## Non-goals

- Ontology content (WP1).
- Production code. Spike code is throwaway and lives under `research/toolchain/spike/`.
- Optimising beyond R-5.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP2-D1 | `research/toolchain/spike/`: the mini-vault, the generator and the measurement scripts, as a uv project | G1–G5 |
| WP2-D2 | `research/toolchain/measurements.md`: timings with machine details, and pasted error outputs | G2, G3 |
| WP2-D3 | `research/toolchain/readout.md`: the recommendation and the OKF verdict | G4–G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| R1 | Every timing and every error output in `measurements.md` was produced by a script in the spike and can be reproduced with one `uv run` command named next to it. | Reviewer reruns two of them |
| R2 | At least two stacks are measured at all three scopes, on the synthetic 500-page vault. | Inspection |
| R3 | OKF was installed and run. The verdict cites what happened, with pasted output. | Inspection |
| R4 | The R-13 mechanism runs: a change to the TBox shows up in the models, or fails the equality test. | Reviewer runs it |

## Definition of good

The recommended stack is the simplest one that meets R-5 and gives the clearest messages.

## Definition of good enough

R1 to R4 met, and the readout lets the ACE pick a stack with evidence.

## Blast radius

`research/toolchain/**` and this file's board rows. Nothing else.

## Agent's defaults

- Python 3.12 and uv. The spike's own `pyproject.toml` lives under `research/toolchain/spike/`, so it doesn't touch the
  package's dependencies.
