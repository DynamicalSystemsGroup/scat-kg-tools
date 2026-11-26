# RS4 — Scope of work: node-page synthesis spike

| | |
|---|---|
| **Status** | Approved by the ACE (log D-132). Runs beside WP22 and WP23; touches none of their files. |
| **Branch** | `spike/node-pages` off `dev`; never merged into `dev`. The readout is merged into `dev` on its own. |
| **Revert point** | none needed (research only) |

## Purpose

The chief engineer asked for help filling in node pages (C12, quoted in `work-packages/candidates.md`; D-123 "a spike
first"): each group, concern, affordance and technology page should be a meaningful synthesis of that concept as it
appears across many narratives, not text copied from one, and the work must avoid naive term matching (different
words can name one concept; one word can name different concepts). Today the tools stub node pages, record edges and
trace them; nothing helps write a node page, and renaming or merging node pages is an accepted gap (W11, D-100). This
spike finds how the tools and the assistant should help, and recommends what to build. Words follow `GLOSSARY.md`.

## Questions

1. **The evidence for one node.** What does a coder (or an assistant) need in front of them to write a node page: every
   narrative that links it, the passages of each account that speak of it, its edges with their narratives, its
   neighbours? Can a view gather this from what the vault already holds (links, the "Edges told" tables, the accounts),
   and what would it return?
2. **Synthesis, not copying.** What does a good node page hold (by type), and what norms keep it a synthesis: written
   across narratives, in the group's or concept's own terms, citing the narratives it draws on, never pasting one
   account? How would an assistant draft one for the coder to accept, within the assistant's rules (A1 to A15)?
3. **Synonyms and homonyms.** How can the tools surface likely cases where two node pages name one concept, or one
   page is used for two concepts, without matching terms naively: for example co-occurrence in the same edges and
   narratives, the coder's own judgement prompted by a review view, or an assistant's proposal the coder confirms?
   What is the smallest safe operation to act on it (merge, split, rename), and how does it keep every narrative's
   table and the knowledge graph conformant?
4. **The shape of the help.** Which parts are a view (the tool), which a skill or MCP prompt (the assistant), which
   an agentic workflow across many pages, and which norms (docs)? What runs on both paths (manual and chat)?
5. **Prior art.** What do qualitative-coding practice (codebooks, memoing, axial coding) and the ontology research
   already in `research/` say about consolidating codes and concepts, and what fits SCAT's layered model?

## Method

Read the vaults the project already has (the template's example, the range vault built from the KOI case, the lab
vaults); try the candidate evidence view as a throwaway script on the range vault; draft one node page of each type by
hand and with a lab assistant (not inference.coop; lab material only, gently paced if any chat is used at all); write
down where synonyms and homonyms appear in the range vault. No change to `src/`, the contracts or the template.

## Deliverables

| Deliverable | Path |
|---|---|
| Readout (at most 1,500 words), with a recommendation and a proposed package | `research/node-pages/readout.md` |
| Notes and throwaway scripts | `spike/node-pages` branch only |

## Requirements

| ID | Requirement | Checked by |
|---|---|---|
| RS4-R1 | Each of the five questions has an answer backed by something tried on a real vault, or is named as open with what would settle it. | The ACE's read; a fresh reviewer |
| RS4-R2 | The recommendation names what is a view, a skill or prompt, a workflow and a norm, and the smallest safe merge/rename operation, with its conformance argument. | The readout |
| RS4-R3 | Nothing outside `research/node-pages/` reaches `dev`; words follow `GLOSSARY.md`. | The diff |

## Definition of good enough

RS4-R1 to R3 met; the ACE can put a v0.1-or-later recommendation to the chief engineer.
