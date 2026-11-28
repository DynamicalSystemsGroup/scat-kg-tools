# Example vault

A small vault for a community tool library: 20 files, one folder per page type, the generated indexes in `index/`, and
`scat.toml` with `stakeholder_group_cap = 3`. Open this folder as a vault in Obsidian 1.9 or later. The draft
narrative is unfinished on purpose (no `description`, no `timeframe`); every other page is complete.

## Every page type
| Type | Pages |
|---|---|
| `group` | `group/volunteer-staff.md`, `borrowers.md`, `funders.md` (a `stub`) |
| `concern` | `concern/safe-handling-of-tools.md`, `quick-checkout.md`, `careful-record-keeping.md` |
| `affordance` | `affordance/self-checkout.md`, `safety-briefing.md` |
| `technology` | `technology/booking-app.md`, `barcode-scanner.md` |
| `narrative` | `narrative/saturday-at-the-lending-desk.md` (a scenario), `self-service-kiosk-pitch.md` (an architecture), `funders-meeting.md` (neither, a `draft`) |
| `index` | `index/group.base`, `concern.base`, `affordance.base`, `technology.base`, `narrative.base` (Bases, not pages) |

## What to look at
1. **A table of edges.** Each narrative has an `## Edges told` table with one row for each edge it tells, both ends
   links. The scenario's table is padded the way Obsidian's editor leaves it; the pitch's is compact and writes the
   type as a slug; the meeting's writes a `\|` in a note.
2. **One pair told twice.** `quick-checkout` is addressed by `self-checkout` in both the scenario and the pitch, each
   with its own note. The knowledge graph holds one edge for it, `done` because both narratives are.
3. **A pair linked in both ends, with no row.** The scenario's account links `volunteer-staff` and `quick-checkout`,
   each an end of a row of its table, and has no row that joins them. The scenario has not said whether it tells that
   edge, so the tool gives no message, and the fingerprint view lists the pair as a candidate. Every node the account
   links is an end of a row: the table is the coding of record.
4. **An edge not yet done.** `funders` holds `careful-record-keeping` is told only by the draft meeting, so the edge is
   not `done`.
5. **A relationship annotation.** `concern/careful-record-keeping.md` has a body line that pulls against
   `quick-checkout`; it has no meaning to the tool.
6. **An alias link in a table.** The pitch's first row writes `[[self-checkout\|the kiosk]]`.
