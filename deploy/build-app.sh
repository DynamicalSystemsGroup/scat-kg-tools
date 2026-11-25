#!/bin/sh
# Build "SCAT Chat.app" from the sources here. The app carries the launcher and the server's source, so it
# works wherever the coder keeps it. Usage: deploy/build-app.sh [output folder]   (default: deploy/build)
set -eu
here=$(cd "$(dirname "$0")" && pwd -P)
root=$(cd "$here/.." && pwd -P)
out=${1:-$here/build}
app="$out/SCAT Chat.app"

command -v osacompile >/dev/null 2>&1 || { echo "build-app: osacompile is missing (it ships with macOS)" >&2; exit 1; }
rm -rf "$app"
mkdir -p "$out"
osacompile -s -o "$app" "$here/SCAT Chat.applescript"

res="$app/Contents/Resources"
cp "$here/scat-chat.sh" "$res/scat-chat.sh"
chmod +x "$res/scat-chat.sh"
ctx="$res/context"
mkdir -p "$ctx/deploy" "$ctx/ontology"
cp "$root/pyproject.toml" "$ctx/pyproject.toml"
cp "$root/ontology/scat.ttl" "$ctx/ontology/scat.ttl"
cp "$here/Dockerfile" "$here/Dockerfile.dockerignore" "$ctx/deploy/"
cp -R "$root/src" "$ctx/src"
find "$ctx" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "built: $app"
