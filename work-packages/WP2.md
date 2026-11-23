# WP2 — Scope of work: Toolchain spike

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md`: G8, R-2, R-5, R-13, and deliverable D-5. |
| **Branch** | Each unit works on `wp2/u<k>`, branched off `dev` and merged back into `dev` (ORG.md). |

## Purpose

Choose the toolchain by measurement before implementation is locked in. The halted first run reported findings,
summarised under "Design guidance" in `MISSION.md`. This run verifies them afresh and doesn't build on them.

## Definitions

- **Neighborhood:** a page, plus every page within one link of it, in either direction.
- **The stacks to measure** (each also needs a parser for markdown with YAML frontmatter and wikilinks):
  - **A:** a pyoxigraph store, with rules as SPARQL queries;
  - **B:** an rdflib store, with rules in SHACL through pyshacl;
  - **C:** no graph store at check time, with rules as pydantic models plus plain Python.

## Goals

- **WP2-G1.** Build a throwaway mini-vault of 15–25 pages. It uses the SCAT classes as `MISSION.md` G1 names them and
  includes scenario and architecture records. It rests on a placeholder TBox at
  `research/toolchain/spike/placeholder-tbox.ttl`, which is not D-1. Also build a generator for a synthetic 500-page
  vault.
- **WP2-G2.** For stacks A, B and C, measure the local, neighborhood and full checks against R-5 on the 500-page vault.
- **WP2-G3.** For each stack, produce the actual messages for four seeded defects, and judge each against R-2 (file,
  field, rule id, an exact fix). The defects:
  - a missing required field;
  - a relation endpoint of the wrong class;
  - a link to a page that doesn't exist;
  - a coded scenario missing a required link type.

  Find out what it takes to make each fix exact, with no placeholders.
- **WP2-G4.** Try OKF hands-on and give a verdict on it as the format between vault and graph.
- **WP2-G5.** Demonstrate one R-13 mechanism, with the placeholder TBox as its source.
- **WP2-G6.** Recommend a toolchain. The recommendation must respect the platform constraint in `MISSION.md`
  Governance.

## Non-goals

- Ontology content (WP1).
- Production code. The spike is throwaway.
- Optimising beyond R-5.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP2-D1 | `research/toolchain/spike/`: a uv project of its own, with the mini-vault, the generator, the placeholder TBox, the stacks, the OKF trial and the R-13 mechanism | WP2-G1 to WP2-G5 |
| WP2-D2 | `research/toolchain/measurements.md`: timings with machine details, and the pasted messages | WP2-G2, WP2-G3 |
| WP2-D3 | `research/toolchain/readout.md`: the recommendation and the OKF verdict | WP2-G4, WP2-G6 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP2-R1 | Every timing and message in `measurements.md` comes from a script in the spike, and reruns with one `uv run` command named next to it. | The reviewer reruns two |
| WP2-R2 | Stacks A, B and C are each measured at all three scopes on the 500-page vault. A stack that can't be run is reported, with the reason. | Inspection |
| WP2-R3 | Each stack's messages for all four defects are pasted, each judged against R-2's four elements. | Inspection |
| WP2-R4 | OKF was installed and run. The verdict cites what happened, with pasted output. | Inspection |
| WP2-R5 | The R-13 mechanism runs: a change to the placeholder TBox either shows up in the models or fails the equality test. | The reviewer runs it |
| WP2-R6 | The mini-vault has 15–25 pages, and one `uv run` command generates the 500-page vault. | `ls`, then the command |
| WP2-R7 | `readout.md` is no longer than 1,000 words. | `wc -w` |
| WP2-R8 | For each defect, `measurements.md` states what it takes to make the fix exact. | Inspection |
| WP2-R9 | The readout lists anything platform-specific (paths, shells, line endings, tools) in the recommended stack, and how it is isolated. | Inspection |

## Definition of good

The recommended stack is the simplest one that meets R-5 and gives the clearest messages.

## Definition of good enough

WP2-R1 to WP2-R9 are met, and the readout names one stack, with the evidence that decided it.

## Blast radius

`research/toolchain/**` only. The spike's `pyproject.toml` and `uv.lock` live under `research/toolchain/spike/`.

## Pre-approved by the ACE

- **Dependencies:** pyoxigraph, rdflib, pyshacl, pydantic, pyyaml, python-frontmatter and pytest, all from PyPI. Any
  other dependency is named in the readout, with the reason.
- **OKF:** install it only from <https://github.com/open-knowledge-format/open-knowledge-format>, pinned to a commit
  recorded in `measurements.md`. Clone it into its own empty directory outside the repository (for example in the session scratchpad), and read
  its install steps and entry points before running anything. Only notes and outputs come into the repository. Run it with paths passed as arguments.
