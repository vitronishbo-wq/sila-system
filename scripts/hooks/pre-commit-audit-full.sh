#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

echo "[pre-commit] Running make audit-full ..."
if ! make audit-full; then
  echo "[pre-commit] Blocked: make audit-full failed."
  exit 1
fi

echo "[pre-commit] OK"
