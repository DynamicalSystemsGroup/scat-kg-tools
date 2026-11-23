# Example vault

A tiny conformant vault for a community tool library: 25 pages, one folder per page type, and `scat.toml` with
`stakeholder_group_cap = 3`. Open this folder as a vault in Obsidian. A check gives one intended warning (the draft).

## Every page type
| Type | Page |
|---|---|
| `stakeholder-group` | `stakeholder-group/volunteer-staff.md` |
| `concern` | `concern/safe-handling-of-tools.md` |
| `affordance` | `affordance/self-checkout.md` |
| `technology` | `technology/booking-app.md` |
| `heldby` | `heldby/volunteer-staff-holds-safe-handling-of-tools.md` |
| `addresses` | `addresses/self-checkout-addresses-quick-checkout.md` |
| `attributes` | `attributes/self-checkout-attributed-to-booking-app.md` |
| `scenario-raw`, `scenario-coded` | `saturday-at-the-lending-desk.md`, `saturday-desk-coded.md` |
| `architecture-raw`, `architecture-coded` | `self-service-kiosk-pitch.md`, `kiosk-pitch-coded.md` |
| `class` | `class/concerns.md` (and six more, one per class) |

Unfinished: `stakeholder-group/funders.md` is a `stub`; `heldby/volunteer-staff-holds-careful-record-keeping.md` is a
`draft` (no `description` yet: a warning, not an error).
## The three capabilities

1. **One concern, two groups.** `safe-handling-of-tools` has two `heldby` pages, one for volunteer staff and one for
   borrowers, each with its own `notes`.
2. **Two concerns in conflict.** `careful-record-keeping` lists `quick-checkout` under `conflicts`. Written once, it
   holds both ways.
3. **Shared concern, differing margins.** Volunteer staff and borrowers share safe handling, then differ: staff hold
   record keeping, borrowers hold quick checkout, and those two are the conflict in 2.
