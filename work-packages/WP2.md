# WP2 — Scope of work: Toolchain spike

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md` (G8, R-2, R-5, R-13, deliverable D-5). |
| **Branch** | `wp2/toolchain-spike`, units off it, merged into `dev` |

## Purpose

Choose the toolchain by measurement, before implementation is locked in. Every stack needs a parser for markdown
with YAML frontmatter and wikilinks, plus one of the stacks below. Separately, we need a single-source schema
mechanism (`MISSION.md` R-13) and a verdict on Open Knowledge Format (OKF) as the format between vault and graph.

## Definitions

- **Neighborhood:** the page, plus every page it links to and every page that links to it (one hop in each
  direction).
- **Stacks measured:**
  - **A:** pyoxigraph store, with rules as SPARQL queries;
  - **B:** rdflib store, with rules in SHACL through pyshacl;
  - **C:** no graph store at check time, with rules as pydantic models plus plain Python.

## Goals

- **WP2-G1.** A throwaway mini-vault of 15–25 pages, using the seven classes `MISSION.md` G1 names, with a placeholder
  TBox at `research/toolchain/spike/placeholder-tbox.ttl` (not deliverable D-1; WP1 decides the real terms). Also a
  generator for a synthetic 500-page vault.
- **WP2-G2.** For stacks A, B and C, measure local, neighborhood and full checks against R-5's thresholds (< 1 s,
  < 2 s, < 5 s on the 500-page vault), on this machine.
- **WP2-G3.** For each stack, produce the actual error output for three seeded defects: a missing required field, a
  relation endpoint of the wrong class, and a link to a missing page. Judge each against R-2: file, field, rule id,
  and an exact fix.
- **WP2-G4.** Try OKF hands-on: install it, run it on the mini-vault, and give a verdict on whether it can be the
  format between vault and graph.
- **WP2-G5.** Demonstrate one R-13 mechanism, with the placeholder TBox as the source: either pydantic models
  generated from it, or a test that the models equal it.
- **WP2-G6.** Recommend a toolchain.

## Non-goals

- Ontology content (WP1).
- Production code. Spike code is throwaway.
- Optimising beyond R-5.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP2-D1 | `research/toolchain/spike/`: the mini-vault, the generator, the placeholder TBox, the stacks, the OKF trial and the R-13 mechanism, as a uv project of its own | WP2-G1 to WP2-G5 |
| WP2-D2 | `research/toolchain/measurements.md`: timings with machine details, and the pasted error outputs | WP2-G2, WP2-G3 |
| WP2-D3 | `research/toolchain/readout.md`: the recommendation and the OKF verdict | WP2-G4, WP2-G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP2-R1 | Every timing and error output in `measurements.md` was produced by a script in the spike and reruns with one `uv run` command named next to it. | Reviewer reruns two |
| WP2-R2 | Stacks A, B and C are measured at all three scopes on the 500-page vault. A stack that can't be made to run is reported with the reason. | Inspection |
| WP2-R3 | Every stack has the error output for each of the three defects, pasted, with a judgement against each of R-2's four elements. | Inspection |
| WP2-R4 | OKF was installed and run, and the verdict cites what happened, with pasted output. | Inspection |
| WP2-R5 | The R-13 mechanism runs: a change to the placeholder TBox either shows up in the models or fails the equality test. | Reviewer runs it |
| WP2-R6 | The mini-vault has 15–25 pages, and one `uv run` command generates the 500-page vault. | `ls`, then the command |
| WP2-R7 | `readout.md` is no longer than 1,000 words. | `wc -w` |

## Definition of good

The recommended stack is the simplest one that meets R-5 and gives the clearest messages.

## Definition of good enough

WP2-R1 to WP2-R7 met, and the readout names one stack with the evidence that decided it.

## Blast radius

`research/toolchain/**` only. `work-packages/board.md` belongs to the PM. The spike's `pyproject.toml` and
`uv.lock` stay under `research/toolchain/spike/`, and repository CI does not check them.

## Pre-approved by the ACE

- **Spike dependencies, from PyPI:** pyoxigraph, rdflib, pyshacl, pydantic, pyyaml, python-frontmatter, pytest. Any
  other dependency is named, with its reason, in the readout.
- **OKF:** install it only from <https://github.com/open-knowledge-format/open-knowledge-format>, at a commit pinned
  and recorded in `measurements.md`. Clone it into its own empty directory under `research/toolchain/spike/okf/` and
  read its install steps and entry points before running anything. Run it with paths passed as arguments, never from
  inside its directory.
