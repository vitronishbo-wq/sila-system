#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

BACKEND_DIR="backend"
if [ -d "apps/backend" ]; then
  BACKEND_DIR="apps/backend"
elif [ ! -d "$BACKEND_DIR" ]; then
  echo "Backend directory not found (expected apps/backend or backend)."
  exit 1
fi

export PYTHONPATH="$PWD/$BACKEND_DIR:${PYTHONPATH:-}"

pytest -q \
  tests/test_architecture_guardrails.py \
  tests/test_institutional_catalog_blueprint.py

pytest -q --noconftest \
  "$BACKEND_DIR/tests/test_alembic_chain.py" \
  "$BACKEND_DIR/tests/test_alembic_health.py" \
  "$BACKEND_DIR/tests/test_catalog_governance.py"

pytest -q tests/test_architecture_guardrails.py \
  -k "identity_consolidation or compat_citizen_repositories"

pytest -q --noconftest "$BACKEND_DIR/tests/e2e/test_matricula_flow.py"
