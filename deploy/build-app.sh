#!/bin/sh
# Build "SCATLAB.app" from the sources here. The app carries the launcher and the server's source, so it
# works wherever the coder keeps it. It is a menu-bar app (no Dock icon, no window), signed ad hoc. Usage: deploy/build-app.sh [output folder]   (default: deploy/build)
set -eu
here=$(cd "$(dirname "$0")" && pwd -P)
root=$(cd "$here/.." && pwd -P)
out=${1:-$here/build}
app="$out/SCATLAB.app"

for tool in osacompile plutil codesign; do
    command -v "$tool" >/dev/null 2>&1 || { echo "build-app: $tool is missing (it ships with macOS)" >&2; exit 1; }
done
rm -rf "$app"
mkdir -p "$out"
osacompile -s -o "$app" "$here/scatlab.applescript"

res="$app/Contents/Resources"
cp "$here/scatlab.sh" "$res/scatlab.sh"
chmod +x "$res/scatlab.sh"
cp "$here/retire-old.sh" "$res/retire-old.sh"
ctx="$res/context"
mkdir -p "$ctx/deploy" "$ctx/ontology" "$ctx/contracts"
cp "$root/pyproject.toml" "$ctx/pyproject.toml"
cp "$root/ontology/scat.ttl" "$ctx/ontology/scat.ttl"
cp "$root/contracts/lifecycle.md" "$ctx/contracts/lifecycle.md"
cp "$here/Dockerfile" "$here/Dockerfile.dockerignore" "$ctx/deploy/"
cp -R "$root/src" "$ctx/src"
find "$ctx" -name __pycache__ -type d -prune -exec rm -rf {} +
# Menu bar only (LSUIElement), then the ad hoc signature (no certificate); this must come last, after every file is in place.
plutil -insert LSUIElement -bool true "$app/Contents/Info.plist"
codesign --force --sign - "$app"
echo "built: $app"
