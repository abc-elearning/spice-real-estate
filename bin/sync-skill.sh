#!/usr/bin/env bash
# bin/sync-skill.sh
# One-way sync: skill/ (source of truth) → .claude/skills/spice-re/deciding-real-estate/
# Excludes .venv and __pycache__ (runtime-only at .claude location)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO_ROOT/skill/"
DEST="$REPO_ROOT/.claude/skills/spice-re/deciding-real-estate/"

if [ ! -d "$SRC" ]; then
  echo "❌ Source directory not found: $SRC" >&2
  exit 1
fi

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "❌ SKILL.md not found in $SRC — refusing to sync" >&2
  exit 1
fi

mkdir -p "$DEST"

rsync -av --delete \
  --exclude='.venv' \
  --exclude='__pycache__' \
  "$SRC" "$DEST"

echo ""
echo "✅ Synced: skill/ → .claude/skills/spice-re/deciding-real-estate/"

if [ ! -d "$DEST/.venv" ]; then
  echo ""
  echo "⚠️  .venv not found at runtime location."
  echo "   Setup: cd $DEST && python3 -m venv .venv && .venv/bin/pip install numpy"
fi
