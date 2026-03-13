#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${BACKEND_DIR}/../.." && pwd)"

if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
  PYTHON_BIN="${REPO_ROOT}/.venv/bin/python"
elif [[ -x "${BACKEND_DIR}/.venv/bin/python" ]]; then
  PYTHON_BIN="${BACKEND_DIR}/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

if [[ -f "${BACKEND_DIR}/.env" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${BACKEND_DIR}/.env"
  set +a
fi

cd "${BACKEND_DIR}"

exec "${PYTHON_BIN}" -m pytest \
  -p pytest_asyncio.plugin \
  --asyncio-mode=auto \
  --confcutdir="${BACKEND_DIR}" \
  app/modules/statistics/tests/test_aggregation.py \
  app/modules/statistics/tests/test_forecasting.py \
  app/modules/statistics/tests/test_statistics_service.py \
  app/modules/statistics/tests/test_integracao_multimodulo_orm.py \
  "$@"
