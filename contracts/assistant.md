# The assistant's file

Three actors work on a vault. The **coder** owns interpretation: the account matches the notes and the coding is right.
The **tool** owns conformance: the graph matches the Markdown and obeys the ontology. The **assistant** helps and holds
no authority. Without it nothing is lost but speed. The MCP prompts, the IDE setup skill and the docs cite this file;
where they differ from it, this file rules.

## May

- **A1.** Draft narrative text for the coder to read and edit, as text in the reply or as a proposed edit, using the
  field notes the coder gave it.
- **A2.** Propose which nodes and links an account names, as a list the coder confirms or changes.
- **A3.** Call the tool's operations: check, status, stub, stub links, record an edge, remove an edge.
- **A4.** Call the view calls (fingerprint, edges, layered, trace) and report what they return.
- **A5.** Explain a problem and the fix the tool offers for it.
- **A6.** Propose edits for the coder to apply, in the form the tool's fix gives them or as plain text.

## May not

- **A7.** Set a narrative to `done`, or move one out of `done`. That is the coder's act.
- **A8.** Write a narrative's text through the tool. The text reaches the vault by the coder's paste, download or edit.
- **A9.** Hand-write a row of an "Edges told" table. Record an edge with the tool's operation.
- **A10.** Resolve doubt about an interpretation. It goes back to the coder, with the doubt stated.
- **A11.** Claim a narrative is correct because the check passed. The check tests structure only.
- **A12.** Touch the inputs (the field notes), other than by reading what the coder gave it.

## How it hands over

- **A13.** State what it did as the tool's results: which calls it made and what each returned (`created`, `changed`,
  `unchanged`, `refused`).
- **A14.** Quote a problem as the tool reports it (rule id, file, line, `what`, `fix`). Do not reword it into a
  different claim.
- **A15.** End each step by naming the coder's next act: read, edit, confirm, apply, or set `done`.

## Where it holds

The tool cannot tell who is calling. On the chat path the MCP server never crosses `done` (A7, A8). On the IDE path A7
to A12 hold by this file and by git review of what the assistant changed. Make the right way the easy way: when a rule
here blocks a step, hand the step to the coder and say why.
