# RS3-U3: tunnel and terminal-free git (D-084)

Dated 2026-11-24. All sources read 2026-11-24, documentation only; nothing installed or signed up for.
V = verified (read in the source); I = inferred. "Not found" means I did not find it.

## Part A. Tunnels

| | Tailscale Funnel | Cloudflare Tunnel | ngrok | Pinggy |
|---|---|---|---|---|
| Cost | Personal plan $0 (V) [1]; Funnel "available for all plans", in beta (V) [2] | Quick: no account or domain (V) [3]. Named: needs a website on Cloudflare (V) [4]; domain cost not checked | Free: one dev domain, 1 GB out and 20k requests a month (V) [5]. Hobbyist $10/month (V) [5] | Free; Pro price not confirmed [6] |
| Account | Yes (I) | Quick no; named yes (V) | Yes, authtoken (V) [7] | Free tunnels: not stated |
| GUI alone? | Docs show only the CLI, `tailscale funnel` (V) [2]. No GUI toggle documented (V) | No. Dashboard gives a command to run in a terminal (V) [4]; install by Homebrew or binary (V) [8] | No. Homebrew, authtoken, `--url` (V) [7][9]. No official Mac app (V) [10] | Site names a desktop app (V) [6] but also says to paste an SSH command into a terminal (V) [6]. Mac support unconfirmed [11] |
| URL stability | Fixed `name.tailnet.ts.net` (V) [2] | Quick: changes every time; no uptime guarantee (V) [3]. Named: fixed | Free dev domain stays the same on restart (V) [12] | Free: 60-minute limit, new URL on restart (V) [6] |
| LibreChat fit | https; ports 443, 8443, 10000 only (V) [2]. Headers: I (Funnel passes requests to the local service) | Quick: no SSE (V) [3], and Streamable HTTP may stream with SSE (I). 200 in-flight cap (V) [3] | Free interstitial is for browser GET only; skipped with a header or custom User-Agent (V) [12]. A server POST should not hit it (I) | Free tunnel dies hourly: unusable |
| What the provider sees | TLS ends on the Mac; relay "cannot decrypt" (V) [2]. Privacy policy: no access to traffic content, but does not mention Funnel (V) [13] | Not stated in pages read; edge likely terminates TLS (I) | Not stated in FAQ [14]; 24-hour request inspector on free (V) [5], so ngrok likely sees content (I) | "Reads tunnel traffic" for its debugger; TLS tunnels are end to end (V) [6] |
| Mac sleeps | Unreachable (I) | Unreachable (I) | Unreachable (I) | Unreachable (I) |

Funnel on macOS is contradictory in the docs. The variants table says Funnel is "no" for App Store and Standalone, "yes" only for the open source build, which has no GUI (V) [15]. The Funnel page says both "you must use one of the open source variants" and that ports can be shared from the App Store or Standalone build (V) [2]. Test before relying on it.

Not researched: localhost.run (fetch refused), hosted relay.

**Recommendation for a non-developer: Tailscale Funnel.** Its URL is fixed, free, port 443 works, and TLS ends on the coder's Mac, so field notes are not readable at the relay. No option is verified terminal-free by documentation. The practical answer is a signed launcher the builder ships, which runs the Funnel command for the coder; whether the Mac app can start the MCP server and that command is a separate question (flag).

**Runner-up: ngrok free.** Fixed free dev domain, a documented browser-only interstitial, but the provider likely sees traffic, and a CLI agent is needed. The 1 GB a month cap could bite on large notes (I).

**Could not verify without installing:**
- Whether Funnel can be switched on from either Mac app (the contradiction above).
- Funnel's bandwidth cap (value not published) against the traffic.
- The one-time browser approval Funnel's CLI triggers (V) [2], which a launcher cannot skip.
- Whether LibreChat accepts a `ts.net` or `ngrok-free` address (allowed-address rules unknown).
- Bot protection or warning pages on Funnel, Cloudflare or Pinggy for server calls.
- Behaviour after sleep and wake.
- Pinggy Mac app, Cloudflare and ngrok data terms.

## Part B. Terminal-free git (private repo from a template)

| Task | GitHub Desktop | github.com | Obsidian Git plugin |
|---|---|---|---|
| Create from template | No: use the web | Yes: "Use this template", pick owner and visibility (V) [17] | No |
| Clone | Yes: Code, "Open with GitHub Desktop", choose folder (V) [18] | n/a | Command exists, URL ends `.git`, clones into a new folder (V) [19]; needs Git installed first (V) [20] |
| Commit and push | Yes (V) [21] | Edit and commit in the browser (I) | Yes, with scheduled commit-and-sync (V) [22] |
| Tag | Yes: History, right-click, Create Tag; pushed with the next push (V) [23] | Yes: Releases, Draft, "Create new tag", Publish (V) [24] | Not found; not documented |
| Private auth | Browser sign-in; token in system keychain (V) [25] | Signed-in browser (I) | Keychain needs `git config` in Terminal plus one authenticated action (V) [20]; or SSH agent (V) [26] |

**Keeping the Mac clone current after web edits.** Desktop: choose the branch, "Fetch origin", then "Pull origin" (V) [27]. Automatic fetch is not in the pages read, so the coder may forget. Obsidian Git pulls on startup and on a schedule (V) [22].

**Recommendation: GitHub Desktop for clone, commit, push and pull, plus github.com for template creation and the version tag or Release.** All steps avoid a terminal and sign-in is one browser step. Tagging from Desktop also works, but the web Release is clearer for a coder (I).

**Runner-up: github.com only** (edit in the browser, no clone), if the tool can read the repo another way. The Obsidian plugin is last: it needs separate Git installation and a Terminal step.

**Not verified:** Desktop's auto-fetch timing; whether the template's private option is offered to this account (the page does not say); Desktop pushing a tag without its commit; Obsidian Git tag support; Xcode tools prompt on Macs without Git.

## Sources
1 tailscale.com/pricing · 2 tailscale.com/kb/1223/funnel and tailscale.com/docs/features/tailscale-funnel.md · 3 developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/ · 4 .../connect-networks/get-started/create-remote-tunnel/ · 5 ngrok.com/pricing · 6 pinggy.io · 7 ngrok.com/docs/getting-started/ · 8 .../connect-networks/downloads/ · 9 web search, ngrok `--url` · 10 ngrok.com/docs/agent/ · 11 pinggy.io/docs/ · 12 ngrok.com/docs/pricing-limits/free-plan-limits/ · 13 tailscale.com/privacy-policy · 14 ngrok.com/docs/faq/ · 15 tailscale.com/docs/concepts/macos-variants · 16 tailscale.com/kb/1242/tailscale-serve · 17 docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template · 18 docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop · 19 publish.obsidian.md/git-doc/Getting+Started · 20 publish.obsidian.md/git-doc/Installation · 21 docs.github.com/en/desktop/overview/getting-started-with-github-desktop · 22 github.com/Vinzent03/obsidian-git · 23 docs.github.com/en/desktop/managing-commits/managing-tags-in-github-desktop (via search results) · 24 docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository · 25 docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/authenticating-to-github-in-github-desktop · 26 publish.obsidian.md/git-doc/Authentication · 27 docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/syncing-your-branch-in-github-desktop
