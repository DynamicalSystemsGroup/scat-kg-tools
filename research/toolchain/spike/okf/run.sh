#!/usr/bin/env bash
# WP2-U4 OKF trial. Reproduces the clone at the pinned commit and runs the trial on a COPY of the mini-vault.
# Usage: bash okf/run.sh   (any cwd). Everything it creates is under okf/{clone,venv,work} (all gitignored).
set -euo pipefail
PIN=527e81aff55992be21507e97004286789126f88c
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT="$HERE/../vault"
CLONE="$HERE/clone"; VENV="$HERE/venv"; WORK="$HERE/work"
PY="$VENV/bin/python"

# clean state
rm -rf "$CLONE" "$VENV" "$WORK"
git clone --quiet https://github.com/open-knowledge-format/open-knowledge-format "$CLONE"
git -C "$CLONE" -c advice.detachedHead=false checkout --quiet "$PIN"
echo "OKF commit: $(git -C "$CLONE" rev-parse HEAD)"

# throwaway env: only PyYAML (OKF's validate.py/scan.py need nothing else; the reference agent's
# google-adk stack is NOT installed, see NOTES.md)
uv venv --quiet "$VENV"
uv pip install --quiet --python "$PY" pyyaml
echo "venv packages:"; uv pip list --python "$PY" 2>/dev/null

mkdir -p "$WORK"; cp -R "$VAULT" "$WORK/vault-copy"
V="$WORK/vault-copy"
VAL="$CLONE/skills/okf-generate/scripts/validate.py"
SCAN="$CLONE/skills/okf-consume/scripts/scan.py"

step() { printf '\n===== %s =====\n' "$*"; }
step "A1 validate.py on the vault copy, as is (wikilinks, spike frontmatter)"
"$PY" -I "$VAL" "$V" || echo "(exit $?)"
step "A2 scan.py on the vault copy"
"$PY" -I "$SCAN" "$V" | head -30 || true
step "A3 scan.py --type Concern"
"$PY" -I "$SCAN" "$V" --type Concern || true
step "A4 baseline wikilinks in vault (independent regex)"
"$PY" -I "$HERE/trial.py" "$CLONE" wikilinks "$V"
step "A5 OKF graph builder on the vault as is"
"$PY" -I "$HERE/trial.py" "$CLONE" graph "$V"
step "A6 OKF document parse->serialize round trip on the vault as is"
"$PY" -I "$HERE/trial.py" "$CLONE" roundtrip "$V"

step "B1 adapter: wikilinks in bodies -> markdown links (frontmatter untouched)"
"$PY" -I "$HERE/wiki2md.py" to-md "$V" "$WORK/bundle"
grep -h "Anonymity" "$WORK/bundle/Facilitators hold Anonymity.md" | head -5
step "B2 validate.py on the converted bundle"
"$PY" -I "$VAL" "$WORK/bundle" || echo "(exit $?)"
step "B3 OKF graph builder on the converted bundle"
"$PY" -I "$HERE/trial.py" "$CLONE" graph "$WORK/bundle"
step "B4 OKF viewer (visualize) on the converted bundle"
"$PY" -I -c "
import sys; sys.path.insert(0, sys.argv[1]+'/src')
from pathlib import Path
from reference_agent.viewer import generate_visualization
print(generate_visualization(Path(sys.argv[2]), Path(sys.argv[3]), bundle_name='mini-vault'))" "$CLONE" "$WORK/bundle" "$WORK/viz.html"
step "B5 round trip: to-md then back to wikilinks, diff against original vault"
"$PY" -I "$HERE/wiki2md.py" to-wiki "$WORK/bundle" "$WORK/back"
diff -r "$V" "$WORK/back" && echo "round trip wikilinks->md->wikilinks: byte-identical"

step "C1 TBox probe: page of unknown class, missing required field, bad status, link to a missing page"
cp -R "$WORK/bundle" "$WORK/probe"
cat > "$WORK/probe/Bogus.md" <<'P'
---
type: NotAClassInTheTBox
status: wibble
---
# Bogus
A concept the placeholder TBox does not know. Links to [Anonymity](Anonymity.md) and [Missing page](Nope.md).
P
grep -v '^description:' "$WORK/probe/Anonymity.md" > "$WORK/a.tmp" && mv "$WORK/a.tmp" "$WORK/probe/Anonymity.md"   # Concern without its required field
head -6 "$WORK/probe/Anonymity.md"
"$PY" -I "$VAL" "$WORK/probe" || echo "(exit $?)"
"$PY" -I "$VAL" --strict "$WORK/probe" >/dev/null && echo "strict: exit 0" || echo "strict: exit $?"
step "C2 spike-vault 'status' vocabulary vs OKF (stub|draft|done vs draft|stable|deprecated)"
"$PY" -I "$HERE/trial.py" "$CLONE" graph "$WORK/probe" | grep status

step "D dependency footprint if the full reference agent were installed (dry run, nothing installed)"
uv pip install --dry-run --python "$PY" "$CLONE" 2>&1 | tail -3
uv pip install --dry-run --python "$PY" "$CLONE" 2>&1 | grep -c '^ + ' || true
step "done"
