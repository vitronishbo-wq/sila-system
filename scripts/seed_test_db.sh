#!/usr/bin/env bash
set -euo pipefail

if [[ "${RUN_DB_INTEGRATION:-0}" != "1" ]]; then
  echo "RUN_DB_INTEGRATION=1 não definido. Seed cancelado."
  exit 0
fi

DB_CONTAINER="${DB_CONTAINER:-sila-db}"
DB_USER="${DB_USER:-sila_user}"
DB_NAME="${DB_NAME:-sila_db}"
SQL_FILE="${SQL_FILE:-apps/backend/seeds/seed_integration_minimal.sql}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ ! -f "${SQL_FILE}" ]]; then
  if [[ -f "${ROOT_DIR}/${SQL_FILE}" ]]; then
    SQL_FILE="${ROOT_DIR}/${SQL_FILE}"
  elif [[ -f "${ROOT_DIR}/apps/backend/seeds/seed_integration_minimal.sql" ]]; then
    SQL_FILE="${ROOT_DIR}/apps/backend/seeds/seed_integration_minimal.sql"
  fi
fi

if [[ ! -f "${SQL_FILE}" ]]; then
  echo "Arquivo SQL não encontrado: ${SQL_FILE}"
  exit 1
fi

echo "Seed de integracao (DB/hierarchy) via Docker..."
docker exec -i "${DB_CONTAINER}" psql -U "${DB_USER}" -d "${DB_NAME}" < "${SQL_FILE}"
echo "Seed concluido."
