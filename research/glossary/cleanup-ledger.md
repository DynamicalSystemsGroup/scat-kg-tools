# WP38 cleanup ledger

Part 1 says what became of every word; part 2 says what became of the 41 inconsistencies. The glossary is
`glossary.yml`; `GLOSSARY.md` and `docs/reference/terms.md` are generated from it (`python3 scripts/glossary.py`).

## Part 1. The words

The glossary now has 53 entries: core 22, plan 7, capture 5, code 12, analyse 6, report 1. Sections are `core` (words
met across the work) and the stages of `contracts/lifecycle.md`, each holding the words first met in that stage's
work. The terms page has 842 words; the test's cap is 927 (842 plus 10%, rounded up), below the old 960.

Counting rule for added words (WP38 default): pages among `docs/*.md` and `docs/reference/*.md` (22 files) other
than `docs/reference/terms.md`, case-insensitive and word-bounded, as RS6 did; 6 or more pages keeps a word.

### Today's 59 words

GLOSSARY.md on `dev` had 55 rows, which hold 61 words once "coded, uncoded", "coder, assistant, tool", "inputs, model,
analysis" and "rule, norm" are split (RS6 counted 59 because it missed `stage` and `transition`, which WP29 added,
and listed `model` twice). Every one of the 61 is here.

| Word | Disposition | Section | Reason |
|---|---|---|---|
| SCAT | kept | core | R2 word. |
| node | kept | core | R2 word. Absorbs "node page" (10 pages). |
| edge | kept | core | R2 word. Absorbs the edge-type spellings: its first sentence names `holds`, `is addressed by`, `is provided by`. |
| element | moved to docs/architecture.md | | RS6: redundant, unused in the docs; an assistant and builder word. |
| layer | kept | core | R2 word. |
| layered graph | moved to docs/architecture.md | | Builder word; RS6: 3 pages or fewer. |
| knowledge graph | moved to docs/architecture.md | | The ABox the tool builds; a builder word. The organiser meets the vault, the page and the view. |
| narrative | kept | core | R2 word. Its second sentence carries what "coded" and "excluded" said (a narrative that links no node page is left out of the views and reported). |
| coded | folded into narrative | | Not R2; the word is retired, the sense is "links a node page". |
| uncoded | folded into narrative | | As "coded". |
| excluded | dropped | | Not R2; the behaviour is in the narrative entry, and the tool's report says it. |
| timeframe | kept | capture | R2 word; the facilitating guide asks it (`facilitate-timeframe.md`). |
| scenario | kept | capture | R2 word; first met in the scenario session guide. |
| architecture | kept | capture | R2 word; first met in the architecture session guide. |
| fingerprint | kept | analyse | R2 word; a view. |
| edge table | kept | analyse | R2 word; a view. |
| layered view | kept | analyse | R2 word; a view. |
| trace | kept | analyse | R2 word; a view. |
| view | kept | analyse | R2 word. |
| relationship annotation | moved to contracts/page-contracts.md | | Not R2; a page-contract detail, in no view. |
| type | kept | core | R2 word. |
| the ontology | moved to docs/architecture.md | | Assistant and builder word; definitions say "the rules" instead. |
| entry | moved to docs/architecture.md | | Builder word (RS6: materially different on the terms page). Definitions say "page". |
| model | moved to docs/architecture.md | | Four senses (RS6 I3); the architecture page keeps the one it needs. |
| conformant | folded into check | | Not R2; "a clean check" and "the check passes" say it. |
| vault | kept | core | R2 word. |
| page | kept | core | R2 word. |
| field | kept | core | R2 word. |
| Edges told | kept | code | R2 word; the test needs the heading. |
| link | kept | code | R2 word; a link is never an edge. |
| cap | kept | plan | R2 word. |
| attribution mode | kept | plan | R2 word. |
| attribution | kept | code | R2 word. |
| contributor page | kept | code | R2 word. |
| index page | kept | report | R2 word; the report stage's output. |
| status | kept | core | R2 word. |
| stage | kept | core | WP38 scope: stage word from WP29. |
| transition | kept | core | WP38 scope: stage word from WP29. |
| mismatch | kept | code | The nine mutation tests of `tests/docs/test_terms.py` need `mismatch` on the terms page (and RS6 found it on 2 pages), so it stays although it is not R2. |
| organiser | folded into coder | | Not R2. The coder entry says the organiser, who runs the elicitation, may also be the coder. Flagged: see "Flagged". |
| coder | kept | core | R2 word; owns interpretation. |
| assistant | kept | core | R2 word; helps, holds no authority. |
| tool | kept | core | R2 word; owns conformance. |
| inputs | moved to docs/architecture.md | | Not R2; RS6 I2 (material kinds disagree). |
| model (the material) | moved to docs/architecture.md | | As "model" above. |
| analysis | moved to docs/architecture.md | | Not R2; four senses (RS6 I4). |
| field notes | kept | capture | R2 word; gathered in capture. |
| interpreting | folded into coding | | Not R2; a step of the coding loop, named in the coding entry. |
| authoring | folded into coding | | As "interpreting". |
| coding | kept | code | R2 word. |
| reviewing | kept | code | R2 word. |
| the coding loop | folded into coding | | Not R2; the coding entry names the loop's four steps. |
| analysing | dropped | | RS6: unused in docs, template, CLI help, MCP text, skills. |
| a finished model | dropped | | RS6: on 1 page; the report stage covers the hand-over. |
| rule | kept | code | R2 word. |
| norm | moved to contracts/assistant.md | | Not R2; guidance for the assistant. |
| skill | moved to contracts/assistant.md | | Assistant word. |
| saved agent | moved to contracts/assistant.md | | Assistant word; RS6: on 2 pages. |
| session key | moved to contracts/assistant.md | | Assistant and builder word; RS6: on 2 pages. |
| leave no trace | dropped | | Not R2; `docs/leave-no-trace.md` defines it where it is used. |
| range vault | moved to docs/architecture.md | | A test fixture; RS6 class ASST. |

### Added words

| Word | Disposition | Section | Reason |
|---|---|---|---|
| session | kept | plan | (d), 17 pages. One sense: a facilitated event. "Start" and "Stop" are not folded in (see below); a chat run is named "a chat run". |
| account | kept | code | (d), 19 pages. Ruling: the narrative's prose, with a link wherever it names a node; no list of links beyond the text (D-205). Absorbs "account text". |
| group | kept | core | (d), 16 pages. |
| concern | kept | core | (d), 15 pages. |
| affordance | kept | core | (d), 13 pages. |
| technology | kept | core | (d), 12 pages. |
| check | kept | core | (d), 21 pages. One entry for the command and the gate; absorbs "clean" (11 pages) and "conformant". |
| clean | folded into check | | (d), 11 pages; "a clean check has no errors" is simpler than an entry. |
| refused | kept | core | (d), 13 pages. |
| coding path | kept | plan | (d), 6 pages. |
| problem | kept | core | (d), 12 pages. Absorbs "error" (10) and "warning" (7). |
| participant | kept | plan | (d), 8 pages. Anyone who takes part in the elicitation. |
| contributor | kept | code | (d), 10 pages. Ruling: a participant whose name a narrative is attributed to; two entries, the simpler. |
| facilitating | kept | capture | (d), 10 pages. |
| node page | folded into node | | (d), 10 pages; "its page is a node page" in the node entry. |
| consent | kept | plan | (d), 10 pages. |
| MCP server | kept | plan | (d), 6 pages; set up with the coding path. |
| Start and Stop | dropped | | (d), 4 and 2 pages (case-sensitive), under 6 pages. Not folded into `session`: the ruling gives `session` one sense. |
| edge type (holds, is addressed by, is provided by) | folded into edge | | (d), 17, 6 and 5 pages; the three verbs are in the edge entry's first sentence, as the test needs. |
| evidence | kept | analyse | (d), 7 pages; a view. |
| REPL | kept | code | (d), 6 pages. |
| mismatch | kept | code | WP38 scope (c); see the first table. |

### The five candidate words (C19)

| Word | Pages | Decision |
|---|---|---|
| orphan | 4 | Not an entry (under 6). |
| plot | 2 | Not an entry (under 6). |
| query result | 1 | Not an entry (under 6). |
| candidate | 7 | Entry, section `code`: two nodes a narrative links that have no row in its `Edges told` table. |
| account text | 3 | Not an entry (under 6); the sense is covered by `account`. |

### Words the moved words need (for the next unit to place)

The next unit places these; this unit did not edit `docs/architecture.md` or `contracts/`.

| Word | Where | One-line definition |
|---|---|---|
| element | docs/architecture.md | A node or an edge. |
| layered graph | docs/architecture.md | The nodes and edges only, in their four layers: the knowledge graph without narratives and relationship annotations. |
| knowledge graph | docs/architecture.md | The nodes, edges and narratives the tool builds from a vault and checks against the ontology, with the contributor pages where the attribution mode allows them. |
| the ontology | docs/architecture.md | The project's fixed definitions of the types and their rules, which the tool checks against; the TBox, in Turtle. |
| entry | docs/architecture.md | One node, edge, narrative or relationship annotation as stored in the vault: a page, or a field on a page. |
| model | docs/architecture.md | The ontology plus a conformant vault; also, as a kind of material, the git repository that holds them. |
| inputs | docs/architecture.md | The field notes: the supplied material. |
| analysis | docs/architecture.md | The reports derived from the model; also the step that reads the views. |
| range vault | docs/architecture.md | A vault that rebuilds a published case with groups, not named people, to test the tools; it is not field data. |
| relationship annotation | contracts/page-contracts.md | A free-text remark between two entries of the same type, written as a body line with a link; not an edge, in no view. |
| norm | contracts/assistant.md | Guidance to coders and assistants, the same for a person as for an LLM, carried in the docs and skill files; the tool does not enforce it. |
| skill | contracts/assistant.md | A package of instructions that an assistant loads and follows; the assistant is still the actor and holds no authority. |
| saved agent | contracts/assistant.md | The chat's feature that keeps an assistant set up for a purpose, so a new chat starts from it. |
| session key | contracts/assistant.md | The key the coder pastes into the chat for one chat run so the chat reaches the tool; kept in the login keychain and deleted at Stop. |

### Flagged

- `organiser` is not in RS6's R2 set and is not an entry; the coder entry defines the organiser in one clause. The
  glossary is for the organiser, so the chief engineer may want it back as an entry.
- `reviewing` (the coder's step) shares a stem with the `review` command (RS6 candidate 21); only the step is defined.
- `contributor` and `participant` are two entries, as the simpler of the two options in the brief.

## Part 2. The 41 inconsistencies

(next unit)
