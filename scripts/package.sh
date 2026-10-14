#!/bin/sh
# Builds dist/<skill>.zip for apps that install a skill from a zip file.
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
"$root/scripts/sync-shared.sh"
rm -rf "$root/dist"
mkdir -p "$root/dist"
cd "$root/skills"
for skill in */; do
  name="${skill%/}"
  zip -qr "$root/dist/$name.zip" "$name" -x "*/__pycache__/*" "*.pyc"
done
cd "$root/dist"
zip -q english-study-skills.zip english-*.zip
echo "Built $(ls "$root"/dist/english-*.zip | wc -l | tr -d ' ') zips in dist/"
