#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "== SILA Sovereign Guardrails =="
echo "Working directory: $(pwd)"

echo "[1/4] Running architecture audit pipeline..."
make audit-full

echo "[2/4] Validating AI bootstrap/context stack..."
python3 scripts/guardrails/check_ai_bootstrap_stack.py --repo-root .

echo "[3/4] Validating core namespace boundaries..."
python3 scripts/guardrails/check_core_namespace.py --root apps/backend

echo "[4/4] Validating module registry synchronization..."
python3 scripts/guardrails/check_module_registry_sync.py --modules-root apps/backend/app/modules

echo "All sovereign guardrails passed."
