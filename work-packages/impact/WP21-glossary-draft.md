# WP21-G9: the glossary draft (for the ACE to log and apply)

Prepared by WP21-U3g. `GLOSSARY.md`, `docs/reference/terms.md` and `tests/docs/test_terms.py` are not edited here. Each
row is in the glossary's own format (term, definition, example use, formal concept and source) and goes in the section
named above its table. Nothing here decides for the ACE beyond one recommendation per collision.

## 1. Proposed entries

### In "The graph and its views" (after **narrative**)

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **coded, uncoded** | Said of a narrative. Coded: it links at least one node page anywhere in its body, in a row end of its Edges told table or in a link in its account. Uncoded: it links none. A coded narrative is in the knowledge graph; an uncoded one is excluded. | "The new narrative is uncoded until it links its first node." | Authored in SCAT; the conformance requirement of WP21-G2 |
| **excluded** | Said of an uncoded narrative: left out of the knowledge graph and every view, and reported as excluded by the check and the views. It is included as soon as it is coded. | "The check reports the draft narrative as excluded: it links no node." | Authored in SCAT; exclusion by the tool, not an error (WP21-G2) |

### In "The vault, as Obsidian shows it" (after **field**)

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **Edges told** | The table on a narrative page under the heading `Edges told`: one row for each edge the account tells, with the columns `from`, `type`, `to`, `note`, each row read as a sentence. Not an edge table. | "Add a row to the Edges told table: parents *hold* bike-safe-for-children." | Authored in SCAT (page contracts); a table of subject, predicate, object |

### In "The work" (after **a finished model**, or grouped as the ACE prefers)

| Term | Definition | Example use | Formal concept and source |
|---|---|---|---|
| **rule, norm** | A rule is what conformance requires and the tool enforces: the catalogue's rules, whose breach the check reports. A norm is guidance to coders and assistants, the same for a person as for an LLM, carried in the docs and in skill files; the tool does not enforce it. | "A narrative with no node link is excluded by a rule; a brief description is a norm." | Rule and norm (authored in SCAT); rule: conformance checking (rule catalogue); norm: guidance of practice (deontic, not enforced) |
| **skill** | A package of instructions that the chat loads for the assistant to follow, The assistant is still the actor and holds no authority. | "Load the SCAT skill before the first reply." | Skill (a feature of the chat; Claude's Agent Skills) |
| **saved agent** | The chat's feature that keeps an assistant set up for a purpose (its instructions, skills and tools) so a new chat starts from it. The assistant is still the actor and holds no authority. | "Start the session from the saved agent for SCAT." | Saved agent (a feature of the chat platform) |
| **session key** | The key the coder pastes into the chat for one session, so the chat reaches the tool. It is kept in the login keychain and deleted at Stop. | "The session key was deleted at Stop." | Bearer token for one session (access control); macOS login keychain |
| **leave no trace** | The strict data-policy option of the chat path's life cycle: a temporary chat, the field notes uploaded as a collection, and the server entry, agents, prompts and skills set up for the session removed from the platform at the end, local copies kept. One option among policies, not a recommendation. | "A project under a non-retention policy may choose the leave no trace life cycle." | Authored in SCAT (WP21-G7); data minimisation (privacy practice) |
| **range vault** | A vault that rebuilds a published case with groups, not named people, to test the tools; it is not field data. | "The KOI range vault passes the check." | Authored in SCAT (test fixture; MISSION) |

## 2. The collision: **edge table**

`GLOSSARY.md` already defines **edge table** as "all edges of one type, between two neighbouring layers, read as a
table" (a view, exported as CSV). G9 asks for a term for the narrative's own table ("Edges told"). Two different tables
would share one word.

- **A. Name the narrative's table "Edges told" and leave **edge table** as it is** (as drafted above). The heading of
  the page is already `Edges told`; the page contracts, catalogue, docs and examples already say "Edges told table".
  One optional clause may be added to the **edge table** row: "Not a narrative's Edges told table." No existing use
  changes.
- **B. Rename the existing **edge table***, for example to "edge export". It changes MISSION (lines 17, 276, 314,
  384), `docs/analysis.md`, `docs/chat-path.md`, `docs/reference/{api,cli,mcp}.md`, `src/scat_kg/{__init__,cli,export}.py`
  and the glossary's **view** row, around the `export-edges` command that already carries the word.

**Recommendation: A.** The words in use already separate the two senses, and B renames a view across about 25 places to
settle a collision nothing yet shows. The ACE decides.

## 3. Sweep: where each word is used today (`git grep -n -i`, excluding `decisions/`, `acceptance/`, `research/`, `work-packages/`, `tests/`, `uv.lock`)

| Word | Where | Any use that would need to change |
|---|---|---|
| uncoded | `contracts/rule-catalogue.md:178` (the retired SCAT-RAW-UNCODED row: "no raw and coded pairs") | None. Historical rows of retired rules. |
| coded | `MISSION.md` 15, 74, 91, 99, 104, 122, 217, 235, 274, 384, 386, 387, 440; `GLOSSARY.md:57` (**status**); `docs/coding.md:66`; `docs/flow.md:14`; `docs/getting-started.md` 13, 205; `ontology/scat.ttl` (retired "raw and coded" notes) | `MISSION.md:74` says a narrative is **done** "when it is coded: every node the account refers to is identified and linked and every edge it tells is recorded". With G9, "coded" means one link or more, which done requires but does not exhaust. Suggest the ACE words MISSION.md:74 as "fully coded", or leaves it as a mission edit for the chief engineer. `MISSION.md` 99 and 104 say "a coded architecture"/"coded scenario" (the retired-word pattern `coded (scenario\|architecture)` of `tests/docs/test_terms.py` does not read MISSION, but would trip on those words in `terms.md`). `GLOSSARY.md:57` ("done: coded and signed off") still reads true. |
| excluded | `contracts/rule-catalogue.md:24`, `src/scat_kg/graph.py:71` ("the separator excluded"; ordinary English) | None. The exclusion rule's own text is another unit's. |
| rule, norm | "rule" is used throughout (catalogue, rules 1 to 4 of section 4, "the rules of the ontology"). "the assistant's rules": `docs/chat-path.md:45, 201`, `docs/ide.md:14`, `docs/reference/mcp.md:55` (`scat://assistant-rules`), `src/scat_kg/mcp_server/prompts.py:5`, `contracts/assistant.md` | `contracts/assistant.md` holds what the assistant may and may not do. The tool does not enforce it, so by the G9 sense it is a norm, yet the docs, the MCP resource and the prompt call it "rules". Flag for the ACE: rename the wording to "norms" in those four places, or define the assistant's file as the one place where "rules" are the assistant's own limits. "norm" has no use today (only "normal"/"normalize"). |
| skill | `MISSION.md` 159, 293, 616; `contracts/architecture.md` 31, 61, 151; `contracts/assistant.md:5`; `docs/chat-path.md:272`; `docs/ide.md` 13 to 24 (the IDE setup skill) | The IDE setup skill is the same kind of thing as the chat's skill (a package of instructions an assistant loads) in a different host. The draft defines the chat's, as asked. If the ACE prefers one entry, widen the definition to "in the IDE or the chat". |
| saved agent | none. `docs/chat-path.md:272-273` says "an agent you set up for SCAT". | Words there would change to "saved agent" when the chat-path guide (G4) is written. |
| session key | `deploy/scat-chat.sh:167` (comment); `deploy/README.md` 10, 11, 17, 23 say "the key"; `deploy/Dockerfile:4` and code use `SCAT_MCP_KEY` | Bare "the key" in `deploy/README.md` would say "session key" once the term is in the glossary. |
| leave no trace | none yet (G7's walkthrough will add it) | None. |
| Edges told | `contracts/page-contracts.md` (heading and rules), `contracts/rule-catalogue.md`, `contracts/architecture.md`, `contracts/assistant.md:21`, `contracts/examples`, `docs/coding.md` (many), 40 hits | None. These already use the heading as the table's name. `terms.md`'s **narrative** row already says "its `Edges told` table". |
| edge table | `GLOSSARY.md` 31, 34; `MISSION.md` 17, 276, 314, 384; `contracts/architecture.md` 14, 62; `docs/analysis.md` 17, 27, 42; `docs/chat-path.md` 231-232; `docs/reference/{api,cli,mcp}.md`; `src/scat_kg/{__init__,cli,export}.py`; `docs/reference/terms.md:18` | All mean the view (all edges of one type). Nothing needs to change under recommendation A. |
| range vault | `MISSION.md:637` ("The range vault rebuilds the KOI case with groups, not named people"); `research/range/koi/` | None. The proposed definition follows MISSION.md:637. |

## 4. Proposed `decisions/log.md` entry (the ACE sets the number and date)

```
## D-nnn | 2026-11-25 | WP21-G9: the glossary gains eleven terms; SCAT-MENTION moves behind an opt-in

The change consultant's sweep (R-18; `work-packages/impact/WP21-glossary-draft.md`) found every use of the words
below. `GLOSSARY.md` gains: coded and uncoded (a narrative is coded when it links at least one node page anywhere in
its body), excluded (an uncoded narrative, left out of the knowledge graph and every view, and reported), rule and
norm (a rule is what conformance requires and the tool enforces; a norm is guidance to coders and assistants, the
same for a person or an LLM, carried in the docs and skill files), skill and saved agent (the chat's features; the
assistant is still the actor), session key (kept in the login keychain, deleted at Stop), leave no trace (the strict
data-policy option, one option and not a recommendation), Edges told (the table of a narrative's edges, columns
`from | type | to | note`), and range vault. The collision of Edges told with the existing edge table (all edges of
one type) is settled by <A: the new term stands and edge table is unchanged | B: edge table is renamed>. Uses
brought in line in this package: <list from the sweep: the assistant's "rules" wording, MISSION.md:74, bare "the key"
in deploy/README.md, "an agent" in docs/chat-path.md>. The same package moves SCAT-MENTION, a link suggestion, out of
the default check: `scat.toml` key `link_suggestions = true` turns it on (default off), and a value that is not a
boolean is refused by SCAT-SUGGEST-CONFIG; off by default like fingerprint candidates (D-101), but a persistent `scat.toml` switch where the candidates are a per-call option, so a "may" is
not graded as a warning. Each change is listed for the chief engineer's review at acceptance.
```

## 5. Effect on `docs/reference/terms.md` and `tests/docs/test_terms.py` (read, not edited)

How they derive: `test_terms.py` reads every bold first-column term of every glossary table (`a, b, c` is three
terms) and every `- **term**:` bullet of `terms.md`, and requires the two sets to be equal. It also holds `terms.md` to
a cap of 600 words, no prescriptive sentence (should, must, need to, do not, you, and so on), no retired word
(including `coded (page|record|scenario|architecture)`), and every backticked name to be in the TBox or in
`CONFIG_NAMES`.

After the ACE applies the draft:

1. `terms.md` needs one bullet per row (`test_terms.py` splits `a, b` rows into separate terms, so eleven terms: coded, uncoded, excluded, Edges told, rule, norm, skill, saved agent, session key, leave no trace, range vault; 2 + 1 + 1 + 2 + 1 + 1 + 1 + 1 + 1 = 11 from nine rows) for `coded, uncoded`, `excluded`, `Edges told`, `rule, norm`, `skill`,
   `saved agent`, `session key`, `leave no trace`, `range vault` (the headings follow the glossary's sections). Until
   they exist `test_terms.py` fails with "the glossary term ... is not defined on the page".
2. `terms.md` is exactly 600 words today, so the eleven terms exceed the cap. The ACE chooses: raise `WORD_CAP` (a
   decision, as WP12 set it), or trim existing bullets. The test needs one line changed in the first case.
3. The bullets must avoid prescriptive words (write "a norm is guidance", not "you should") and the phrase
   "coded scenario"/"coded architecture". Backticking `Edges told` is allowed (a TBox table heading).
4. `CONFIG_NAMES` is `{"scat.toml", "stakeholder_group_cap"}`. If a `terms.md` bullet backticks the new key
   `link_suggestions` it must be added there; the bullets above do not need it, so no change.
5. If the ACE takes option B (rename edge table), the test follows the glossary with no edit, but `terms.md`'s
   `edge table` bullet and `docs/` uses move with it.
