# w3id.org registration for https://w3id.org/scat

## What this is

The scat-kg ontology IRI is `https://w3id.org/scat` and its terms live in the namespace `https://w3id.org/scat#`. That IRI is not yet registered. This file holds the exact content of one pull request to the w3id.org registry that registers it. The team submits nothing. The chief engineer submits it, from his own fork.

## Pull request content (copy exactly)

Two files, in the folder `ids/scat/`.

### File 1: ids/scat/.htaccess

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

### File 2: ids/scat/README.md

```markdown
# /scat/

Permanent identifier for the scat-kg ontology. Terms are in the namespace `https://w3id.org/scat#`.

- `https://w3id.org/scat` with `Accept: text/turtle` redirects to <https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/main/ontology/scat.ttl>
- `https://w3id.org/scat` for any other request to the bare identifier redirects to <https://dynamicalsystemsgroup.github.io/scat-kg-tools/>

## Contacts

- Dynamical Systems Group
  - GitHub: [@mzargham](https://github.com/mzargham)
```

## Notes for the submitter (not part of the pull request)

### When to submit

Submit only after the release pull requests are merged and this command prints `HTTP/2 200` (the registry's guide requires the redirect target to be live over HTTPS before the pull request is opened):

```sh
curl -sI https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/main/ontology/scat.ttl
```

On 2026-11-23 it returned 404, because the file reaches `main` only with the release merge. The docs site answered 200 on the same date. The ontology's rdfs:comment still says "The IRI base is unregistered until release." and will be out of date once this merges.

### How to submit

1. Read the registry's scope page first: https://github.com/perma-id/w3id.org/blob/master/docs/overview/scope.md . Confirm you are content for the GitHub handle `mzargham` to be public in the pull request.
2. Read the registry's instructions: https://github.com/perma-id/w3id.org/blob/master/docs/guides/create-an-id.md and https://github.com/perma-id/w3id.org/blob/master/docs/guides/content-negotiation.md .
3. Fork https://github.com/perma-id/w3id.org on GitHub.
4. Create the two files above. The registry keeps identifiers under `ids/`, so the folder is `ids/scat/`, not `scat/` at the repository root. In the GitHub web editor, type the whole path `ids/scat/.htaccess` into the filename box, or GitHub refuses a name that starts with a dot.
5. Squash to one commit. Suggested message: `scat: add redirect for ontology namespace`.
6. Open the pull request against `perma-id/w3id.org`. Touch nothing outside `ids/scat/`.

On 2026-11-23 `ids/scat` did not exist in the registry, so the name was free then. Look again before submitting.

### What the rules do

Status 303 See Other: the registry's guidance says to use 303 for content-negotiated ontology IRIs, because the IRI names the ontology and the target is a document about it. The Turtle condition is tested first and the unconditional docs rule is last, as the guidance requires.

The rules match only the bare `https://w3id.org/scat/`. A `#Term` fragment never reaches the server, so `https://w3id.org/scat#Term` is the same request as the bare one. Any sub-path, such as `/scat/Term`, matches no rule and returns 404 from the registry. Within the bare request, `text/turtle` goes to the raw Turtle file and everything else goes to the docs site.

### Check after the pull request merges

Merging can take a while to deploy. Run these until they answer.

```sh
curl -sI -H 'Accept: text/turtle' https://w3id.org/scat
curl -sI https://w3id.org/scat
```

Expected, to confirm after merge: each answers `301 Moved Permanently` with `Location: https://w3id.org/scat/`. This was seen on a local Apache and on another registry entry, not yet on this one. Then run the slash form, which shows the rules:

```sh
curl -sI -H 'Accept: text/turtle' https://w3id.org/scat/
curl -sI https://w3id.org/scat/
```

| Command | Status | Location header |
| --- | --- | --- |
| Turtle, with slash | `303` | `https://raw.githubusercontent.com/DynamicalSystemsGroup/scat-kg-tools/main/ontology/scat.ttl` |
| Plain, with slash | `303` | `https://dynamicalsystemsgroup.github.io/scat-kg-tools/` |

Then fetch the Turtle location itself with `curl -sI`. It must answer `200`.
