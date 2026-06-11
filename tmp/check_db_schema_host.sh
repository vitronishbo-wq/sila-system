#!/usr/bin/env bash
set -euo pipefail

export PGPASSWORD="Trumanmarcelo_1983"
HOST=127.0.0.1
USER=sila_user
DB=sila_db

TABLES=(locations territories territory_closure educacao_escolas educacao_turmas educacao_matriculas educacao_academic_identities educacao_boletins educacao_certificados educacao_institution_capacities)

for t in "${TABLES[@]}"; do
  echo
  echo "=== $t ==="
  psql -h "$HOST" -U "$USER" -d "$DB" -Atc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name = '$t';"
done
