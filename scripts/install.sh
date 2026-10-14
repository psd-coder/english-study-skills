#!/bin/sh
# Installs the english-study skills from a release zip into an agent's skills folder.
#   curl -fsSL <repo-raw-url>/scripts/install.sh | sh -s -- claude
# Targets: claude (~/.claude/skills), codex (~/.codex/skills), agents (~/.agents/skills),
# or a folder path.
set -eu
repo="${ENGLISH_STUDY_REPO:-psdcoder/english-study-skills}"
target="${1:-claude}"
case "$target" in
  claude) dest="$HOME/.claude/skills" ;;
  codex) dest="$HOME/.codex/skills" ;;
  agents) dest="$HOME/.agents/skills" ;;
  *) dest="$target" ;;
esac
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
curl -fsSL "https://github.com/$repo/archive/refs/heads/main.tar.gz" | tar -xz -C "$tmp"
src="$(find "$tmp" -maxdepth 1 -mindepth 1 -type d | head -n 1)"
sh "$src/scripts/sync-shared.sh" >/dev/null
mkdir -p "$dest"
for skill in "$src"/skills/*/; do
  name="$(basename "$skill")"
  rm -rf "${dest:?}/$name"
  cp -R "$skill" "$dest/$name"
done
echo "Installed english-study skills into $dest"
echo "Start with: \"I want to study English\" in your agent."
