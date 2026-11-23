# WP3 — Scope of work: Facilitation research spike

| | |
|---|---|
| **Status** | Approved by the ACE when the decision log records it. Runs inside `MISSION.md`: G11, R-14, and deliverable D-5. |
| **Branch** | Each unit works on `wp3/u<k>`, branched off `dev` and merged back into `dev` (ORG.md). |

## Purpose

Derive, from prior work, the facilitation strategy that the planning guide and the two facilitation guides will be
written from. The strategy covers:
- the improvisational stance ("yes, and"; "from this perspective");
- how to elicit behavioural scenarios and structural architectures;
- how to hold disagreement, and margins of potential conflict, without adjudicating.

It also gives the TBox design (WP4) what the facilitation side needs the graph to be able to show.

## Goals

- **WP3-G1.** Distil what the sources say about:
  - eliciting stories and proposed designs;
  - keeping multiple perspectives;
  - exposing controversy, friction, gaps and dissent;
  - the risks of collapsing disagreement.

  The sources:
  - `ant-rdf` (<https://github.com/mzargham/ant-rdf>): its vocabulary and briefs on controversy, translation,
    perspective and dissent;
  - "KOI & The Unicorn" (<https://blog.block.science/koi-and-the-unicorn/>);
  - "Building the Loop" (EPIC 2025, DOI 10.1111/epic.70009);
  - the unpublished grant-proposal drafts from the same collaboration, read for principles only. Their location is
    given in the unit's private brief, never in this repository.
- **WP3-G2.** Write a facilitation strategy, organised by the journey: planning an event (J4), capturing scenarios
  and architectures (J5), and what coding needs from capture (J6). Write it in our own words, with improvisational
  jazz as its idiom.
- **WP3-G3.** List what the graph must be able to show for the strategy to work: for example, the same concern held
  by different groups, and concerns in tension. This is input to WP4, not a design.

## Non-goals

- Writing the docs guides themselves (WP7).
- Ontology terms or the TBox (WP1, WP4).
- Methods for ranking, voting or reaching consensus, beyond noting that they are out of scope.
- Quoting or linking private documents.

## Deliverables

| ID | Deliverable | Serves |
|---|---|---|
| WP3-D1 | `research/facilitation/sources.md`: per published source, what it contributes, with citations; the private drafts summarised for principles only, without quotes or links | WP3-G1 |
| WP3-D2 | `research/facilitation/strategy.md`: the strategy, organised by J4, J5 and J6 | WP3-G2 |
| WP3-D3 | `research/facilitation/readout.md`: the strategy in brief, plus the list for WP4 | WP3-G2, WP3-G3 |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| WP3-R1 | Every claim drawn from a published source cites it. Nothing from the private drafts is quoted or linked, and no private detail (people, budgets, funder specifics) appears. | The reviewer checks the citations and greps the deliverables for the drafts' titles and for names (both supplied in the reviewer's private brief) |
| WP3-R2 | The strategy contains no step that ranks, votes on or adjudicates between stories or architectures (R-14). | Inspection |
| WP3-R3 | The strategy covers J4, J5 and J6, and for J5 treats scenarios (behavioural) and architectures (structural) separately. | A checklist |
| WP3-R4 | The list for WP4 names capabilities, not terms or mechanisms. | Inspection |
| WP3-R5 | `readout.md` is no longer than 1,000 words. | `wc -w` |
| WP3-R6 | `sources.md` covers each source against each of the four WP3-G1 topics (or says the source is silent on it). | A checklist |
| WP3-R7 | `strategy.md` makes the stance concrete in each of J4, J5 and J6: what "yes, and" and "from this perspective" look like at that stage. | A checklist |

## Definition of good

A facilitator could run a session from the strategy and feel the "yes, and". Nobody would be argued into agreement,
and nothing anyone said would be lost.

## Definition of good enough

WP3-R1 to WP3-R7 are met. The list for WP4 includes at least the same concern held by different groups and concerns
in tension, and the readout gives WP7 a pointer for each of J4, J5 and J6.

## Blast radius

`research/facilitation/**` only.

## Agent's defaults

- Units:
  - one reading `ant-rdf`;
  - one reading the two published essays;
  - one reading the private drafts;

  then a synthesis unit.
- The private-drafts unit works through the Google Drive connector, read-only. Its notes never leave the unit's
  report unless they're summarised as principles.
