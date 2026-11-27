# Data, rights and consent

This page names the operational choices that later steps depend on. It makes none of them and gives no legal advice.
Who holds the rights to each kind of material, and what the law or an ethics board requires, is not decided here. The
organiser, and the organisation or board the organiser answers to, decide it. Every example is one answer among 2 or 3, and the examples are not the only answers. An answer of your own is fine when it says what you will do, for which kind of material, and for whom (a client, a funder, the participants, or no one); a choice can have a different answer for each kind of material, and a licence or a rights split you make up is as good as one listed.

SCAT holds three kinds of material, and an answer can differ for each: the **inputs** (the field notes, and the
narratives drafted from them), the **model** (the git repository: narratives, nodes, edges, the [knowledge graph](reference/terms.md)) and
the **analysis** (derivative reports, such as documents with excerpts, data or figures). A narrative that quotes the field
notes carries that text into the model, and the rules for the model then apply to it.

## What the tool does

- The four layers name groups, never individuals. The cap on groups, set in `scat.toml` by the person who set up your tools, is enforced: the tool
  refuses a group page beyond it.
- Whether a narrative names the people it is attributed to is the vault's attribution mode, also set in `scat.toml`
  and enforced. See [Attribution mode](#attribution-mode).
- The `scat` commands read and write the vault folder and make no network calls. They do not read the field notes.
- The tool cannot tell whether a person or an assistant wrote a page.
- Consent has no field in the vault. The consent records are inputs, kept as choice 3 and choice 2 say. Git keeps every committed version of a page.

## The choices

Nine, made before the first session. Each is a dependency: a later step is planned from the answer.

1. **What is collected, and in what form.** Planning (step 6) and capture (step 7) depend on it. For example: audio
   recordings and a transcript; handwritten notes typed up; typed notes only.
2. **Where it is stored, and who can see it.** Setup (step 5) depends on it. The template's default is a private
   repository on GitHub, visible to the owner and the people invited. For example: that repository alone; a separate
   private repository for the inputs; an encrypted drive for recordings.
3. **Consent, and how it is documented.** Capture depends on it. SCAT describes consent as informed: the organisers
   choose the participation terms up front, every participant works within the same terms, and they are told before
   they take part. For example: a signed form each; a read-aloud statement recorded in the notes; the terms in the
   invitation.
4. **What contributions will and will not be used for.** Analysis (step 9) depends on it. Attribution is part of it:
   the answer fixes the vault's attribution mode (see [Attribution mode](#attribution-mode)).
   For example: the Chatham House rule; attribution by name with permission; use for the funder's report only.
5. **Whether AI is used, and which tools may touch which data.** Coding (step 8) depends on it, and the answer is
   matched to what participants were told. On the chat path the field notes go to the chat provider's service. For
   example: no AI; an approved service on the inputs only; an approved service on the model, not the inputs.
   If the answer is a strict policy (nothing may stay on the AI platform), see [Leave no trace](leave-no-trace.md).
6. **Who the material is released to, and in what form.** Hand-over (step 10) depends on it. Release has levels between
   private and public. Publishing the analysis and publishing the field notes are separate questions. For example:
   contributors only; the analysis public, the inputs private; nothing released.
7. **Under what licence anything is published.** Hand-over depends on it. The tools' Apache-2.0 licence covers the
   tools, not the data. For example: CC BY 4.0; CC BY-NC 4.0; none, as nothing is published.
8. **Who holds the rights to each kind of material.** Hand-over depends on it. For example: the organiser's
   organisation; the participants; a funder.
9. **How commitments to participants are followed through.** What comes after hand-over depends on it. For example: a
   findings session with contributors; a written summary sent to each; a copy of the released analysis.

## Attribution mode

Choice 4 fixes one setting for the whole vault, the **attribution mode**. The person who set up your tools writes it in `scat.toml` before the first
session, and the check refuses a vault that has none. The mode says whether a narrative names the people it is
attributed to. It is the same for every participant, so say which one it is in the consent you gather.

| Mode | What participants are told | What the vault holds |
|---|---|---|
| `required` | Each account is attributed to the person who gave it, by name. | A contributor page for each person named. Every narrative names its contributors before it is `done`. |
| `optional` | Each account is attributed to its giver only if that person wants it. | A contributor page for each person who chose to be named. A narrative names its contributors or names none. |
| `disallowed` | No account is attributed to anyone. The Chatham House rule is this mode. | No contributor page, and no narrative names a contributor. The tool refuses both. |

Contributor pages exist only in `required` and `optional` vaults. The four layers hold groups in every mode. A contributor
page holds a name or handle you record, so in those two modes the vault holds people's names, and the answers to choices 2
and 6 cover them. [Planning](planning.md#choose-the-attribution-mode) shows what to say aloud for each mode, and
[Coding](coding.md#contributor-pages-and-attributed_to) shows the pages.

## Before you start

One question for each choice above, to tick when it is documented.

- [ ] What will be collected, and in what form?
- [ ] Where is each kind of material kept, and who can see it?
- [ ] How is consent given and documented?
- [ ] What will contributions be used for, and not used for? Which attribution mode follows from it?
- [ ] Is AI used, and which tools may touch which data?
- [ ] Who is each kind of material released to, and in what form?
- [ ] Under what licence is anything published?
- [ ] Who holds the rights to each kind of material?
- [ ] How are commitments to participants followed through?

Keep your answers with the consent records, outside the vault.
