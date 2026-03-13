#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HOOK_SRC="$REPO_ROOT/scripts/hooks/pre-commit-audit-full.sh"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit"

if [[ ! -f "$HOOK_SRC" ]]; then
  echo "Hook source not found: $HOOK_SRC"
  exit 1
fi

install -m 0755 "$HOOK_SRC" "$HOOK_DST"
echo "Installed pre-commit hook: $HOOK_DST"
