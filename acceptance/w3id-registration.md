# w3id.org registration for https://w3id.org/scat

## What this is

The scat-kg ontology IRI is `https://w3id.org/scat` and its terms live in the namespace `https://w3id.org/scat#`. That IRI is not yet registered. This file holds the exact content of one pull request to the w3id.org registry that registers it. The team submits nothing. The chief engineer submits it, from his own fork.

## How to submit

1. Fork https://github.com/perma-id/w3id.org on GitHub.
2. Read the registry's own instructions first: https://github.com/perma-id/w3id.org/blob/master/docs/guides/create-an-id.md and https://github.com/perma-id/w3id.org/blob/master/docs/guides/content-negotiation.md .
3. In the fork, create the two files below. The registry now keeps identifiers under `ids/`, so the folder is `ids/scat/`, not `scat/` at the repository root. In the GitHub web editor, type the whole path `ids/scat/.htaccess` into the filename box, or GitHub refuses a name that starts with a dot.
4. Squash to one commit. Suggested message: `scat: add redirect for ontology namespace`.
5. Open the pull request against `perma-id/w3id.org`. Touch nothing outside `ids/scat/`.

At the time of writing (2026-11-23) `ids/scat` did not exist in the registry, so the name was free.

## File 1: ids/scat/.htaccess

Status 303 See Other: the registry's guidance says to use 303 for content-negotiated ontology IRIs, because the IRI names the ontology and the target is a document about it. The condition `text/turtle` is tested first and the unconditional docs rule is last, as the guidance requires. The fragment form `https://w3id.org/scat#Term` needs no rule of its own: the browser strips `#Term`, so the server sees `/scat/`. The same holds with and without the trailing slash, whose first hop is the registry's own 301 to the slash form.

```apache
# # /scat/
#
# Content-negotiated IRI for the scat-kg ontology (namespace https://w3id.org/scat#).
#
# A request that accepts text/turtle goes to the ontology file on the main branch of
# https://github.com/DynamicalSystemsGroup/scat-kg-tools
# Every other request goes to https://dynamicalsystemsgroup.github.io/scat-kg-tools/
#
# ## Contact
# This space is administered by:
#
# Dynamical Systems Group
# GitHub username: mzargham

RewriteEngine on

# Turtle
RewriteCond %{HTTP_ACCEPT} text/turtle
RewriteRule ^$ https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/main/ontology/scat.ttl [R=303,L]

# Everything else, including browsers: the documentation site
RewriteRule ^$ https://dynamicalsystemsgroup.github.io/scat-kg-tools/ [R=303,L]
```

## File 2: ids/scat/README.md

```markdown
# /scat/

Permanent identifier for the scat-kg ontology. Terms are in the namespace `https://w3id.org/scat#`.

- `https://w3id.org/scat` with `Accept: text/turtle` redirects to <https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/main/ontology/scat.ttl>
- `https://w3id.org/scat` for every other request redirects to <https://dynamicalsystemsgroup.github.io/scat-kg-tools/>

## Contacts

- Dynamical Systems Group
  - GitHub: [@mzargham](https://github.com/mzargham)
```

## Check after the pull request merges

Merging can take a while to deploy. Run both commands until they answer.

```sh
curl -sI -H 'Accept: text/turtle' https://w3id.org/scat
curl -sI https://w3id.org/scat
```

The registry first answers `301 Moved Permanently` with `Location: https://w3id.org/scat/`. This is normal. Then run the slash form, which shows the rules:

```sh
curl -sI -H 'Accept: text/turtle' https://w3id.org/scat/
curl -sI https://w3id.org/scat/
```

| Command | Status | Location header |
| --- | --- | --- |
| Turtle, with slash | `303` | `https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/main/ontology/scat.ttl` |
| Plain, with slash | `303` | `https://dynamicalsystemsgroup.github.io/scat-kg-tools/` |

Then fetch the Turtle location itself with `curl -sI`. It must answer `200`.

## When it works

On 2026-11-23 I fetched the raw Turtle URL on `main`: `curl -sI https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/main/ontology/scat.ttl` returned HTTP 404. The file reaches `main` only when the release pull request merges. So:

- The docs redirect works now: the docs site answered 200 on the same date.
- The Turtle redirect will be correct from the day the registry merges, but it leads to a 404 until the release merge. Submit this pull request now or after the release merge. If after, the registry reviewers will find a live target, which their guide asks for.
- The ontology file currently says the IRI base is unregistered. After the release merge, that text is out of date.
