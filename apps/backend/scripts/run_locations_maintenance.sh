#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

: "${POSTGRES_HOST:=localhost}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_USER:=sila_user}"
: "${POSTGRES_DB:=sila_db}"

psql "host=${POSTGRES_HOST} port=${POSTGRES_PORT} user=${POSTGRES_USER} dbname=${POSTGRES_DB}"   -v ON_ERROR_STOP=1   -f "${SCRIPT_DIR}/normalize_locations_title_case.sql"

python "${SCRIPT_DIR}/locations_audit.py"
