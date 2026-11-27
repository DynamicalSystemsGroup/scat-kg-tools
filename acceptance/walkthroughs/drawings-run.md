# Run record: drawings returned by the server (WP28-R5)

Run 27 Nov 2026 in the chief engineer's sitting: SCAT Chat rebuilt from tools `dev` a2f089c (the server with
`draw_fingerprint`, `draw_layered`, `draw_trace`), serving the lab vault `my-vault`; the ACE as coder; his accounts
and keys. Screenshots are in the sitting's evidence folder (`r5/`), outside the repository.

| Client | Header form | Connected | Image shown | Notes |
|---|---|---|---|---|
| Claude (claude.ai) | `x-api-key` with the key alone | yes, 22 tools listed | yes: the `draw_layered` PNG inline in the reply and in Claude's image panel ("Image · PNG", Download as PNG) | |
| Claude (claude.ai) | `authorization` with `Bearer <key>` | no: "Couldn't reach SCAT", entry "Not connected" | n/a | Same failure as the morning's run, same key and setup; the server accepts Bearer (its key-gate tests), so Claude does not deliver that header as the server needs. The chat path's page keeps `x-api-key` (tools 3ba11c2). |
| inference.coop (chat) | API Key, Bearer format | yes ("SCAT - Connected") | yes: the `draw_layered` PNG (1270 x 350) inline under the tool call; the model read its `(stub)` tags and footer | The model also wrote its own markdown image link to the picture, shown as a broken placeholder. Asked by the chief engineer for "some fingerprints and some traces", the model chose `format` svg, got SVG text back, said it could not display it, and read the drawings' coordinates instead (its reading agreed with the text views). |

Findings for later packages: the assistant should ask for PNG to show a picture and SVG only to save one, and should
not re-embed a tool's image (inputs to WP30's analysis guide and WP31's habits).
