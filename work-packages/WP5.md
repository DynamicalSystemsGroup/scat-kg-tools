# WP5 — Scope of work: Conformance tools

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md`: G2, G3, G4, G5 (the tools half), R-1 to R-5, R-7, R-8, R-13, the platform constraint, and deliverable D-2. |
| **Branch** | Each unit works on `wp5/u<k>`, branched off `dev` and merged back into `dev` (ORG.md). |
| **Inputs** | `ontology/scat.ttl`, `contracts/page-contracts.md`, `contracts/rule-catalogue.md`, `contracts/examples/`, `research/toolchain/` (stack C), and log D-028, D-031 and D-032 |

## Purpose

Build the `scat_kg` package and the `scat` CLI on the toolchain WP2 chose (stack C), implementing WP4's contracts
and rule catalogue, so that a facilitator-analyst can check and work on a vault from the Python REPL or the terminal.
Set up the package and its CI so that the template can install it pinned to a commit.

## Goals

- **WP5-G1. Package and CI.** `scat-kg-tools` becomes an installable uv project: the package `scat_kg`, the CLI
  `scat`, and the TBox shipped with the package so that it is the tools' single source (R-13). It has CI on GitHub
  Actions, per the mission's Agent's defaults: locked sync, lock check, ruff, pytest, and an attribution check.
- **WP5-G2. Reading a vault.** Parse pages (YAML frontmatter, wikilinks in fields and bodies) into the ABox the
  contracts describe, and address pages by name or by path, as the contracts specify.
- **WP5-G3. Checks.** Implement every rule in the catalogue at its severity, at three scopes: a page, its
  neighborhood, and the whole vault.
- **WP5-G4. The other operations.** Read status at the three scopes, set a page's status, regenerate the class
  indexes, and create stubs, including relation pages for pairs the author names (D-031). The Python API and the CLI
  offer every operation with the same messages (R-8).
- **WP5-G5. The TBox gap from D-032.** Add the relation endpoint order to `ontology/scat.ttl` as stated triples, and
  read it from there.

## Non-goals

- The template repository and the case study (WP6). The docs site (WP7).
- New rules, or changes to rule severity or meaning, beyond the catalogue. A gap found during implementation goes to
  the ACE.
- Publishing to PyPI. Any graph store at check time.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP5-D1 | `pyproject.toml`, `uv.lock`, `.python-version`, `.github/workflows/` | WP5-G1 |
| WP5-D2 | `src/scat_kg/`: the package, the API and the CLI | WP5-G2 to WP5-G4 |
| WP5-D3 | `tests/`: seeded-defect fixtures and tests, snapshot tests, both-path tests, the R-13 test or generator, and a benchmark that generates its own 500-page vault | all |
| WP5-D4 | The endpoint-order triples in `ontology/scat.ttl` | WP5-G5 |

## Requirements

These are `MISSION.md`'s requirements, made specific to this package.

| ID | Requirement | Checked by |
|---|---|---|
| WP5-R1 | Every catalogue rule has at least one seeded-defect test that triggers it at its stated severity, and errors block while warnings don't (R-1). | The test suite; a script that lists rule ids without a test (expected empty) |
| WP5-R2 | Every message names the file, the field or link, and the rule id, and gives the catalogue's exact fix (R-2). Golden tests compare those four elements, not the full prose. | Golden tests |
| WP5-R3 | Status behaves as R-3 and the catalogue say. | Tests per status |
| WP5-R4 | Checks never write. Every write is an explicit operation (R-4). | Tests that snapshot the vault before and after each operation |
| WP5-R5 | R-5's thresholds are met on a generated 500-page vault. | `uv run` benchmark, with output pasted in the PR |
| WP5-R6 | Every operation is available from the Python API and the CLI, with the same messages (R-8). | Tests that run both paths on the same fixtures |
| WP5-R7 | The models the checks use are generated from the TBox, or held equal to it by a test that covers slugs, descriptions, fields, status values, link rules and endpoint order (R-13). | The generator or test, in CI |
| WP5-R8 | Every page in `contracts/examples/` checks clean, except where an example is meant to show a warning. | A test |
| WP5-R9 | CI runs on every push and is green at delivery. The package installs from a git commit with `uv`, in a fresh directory. | The CI run; a clean-install trial, with output pasted |
| WP5-R10 | Nothing puts Linux or Windows support at risk: paths through `pathlib`, no shell calls, UTF-8 and line endings handled, and filename rules as the contracts state. | The reviewer's inspection; CI on Linux |

## Definition of good

A facilitator-analyst can work a whole session from the REPL or the terminal, and every message tells them exactly
what to do. The code is small enough for one person to maintain, and reads as a direct implementation of the
contracts.

## Definition of good enough

WP5-R1 to WP5-R10 are met.

## Blast radius

`pyproject.toml`, `uv.lock`, `.python-version`, `src/**`, `tests/**`, `.github/**`, and the endpoint-order triples
in `ontology/scat.ttl`. Nothing else.

## Agent's defaults

- CLI framework: the standard library's `argparse` unless the PM finds a strong reason otherwise, to keep the
  dependencies to pydantic and PyYAML.
- The build backend ships `ontology/scat.ttl` inside the wheel. It is never copied by hand.
