#!/bin/sh
# Builds dist/english-study.zip, the plugin file for apps that install a plugin from a zip.
set -eu
root="$(cd "$(dirname "$0")/.." && pwd)"
rm -rf "$root/dist"
mkdir -p "$root/dist"
cd "$root"
zip -qr dist/english-study.zip .claude-plugin plugin.json skills shared LICENSE \
  -x "*/__pycache__/*" "*.pyc" "*.DS_Store" "shared/test_study.py"
echo "Built dist/english-study.zip"
