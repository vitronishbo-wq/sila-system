#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT/apps/backend${PYTHONPATH:+:$PYTHONPATH}"
pytest --confcutdir="$SCRIPT_DIR" "$SCRIPT_DIR" "$@"
