#!/bin/sh
# Each skill installs on its own, so each one carries a copy of shared/.
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
for skill in "$root"/skills/*/; do
  rm -rf "$skill/shared"
  mkdir -p "$skill/shared"
  cp "$root"/shared/study.py "$root"/shared/*.md "$skill/shared/"
done
echo "Synced shared/ into $(ls -d "$root"/skills/*/ | wc -l | tr -d ' ') skills"
