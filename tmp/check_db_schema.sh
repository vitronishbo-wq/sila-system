#!/usr/bin/env bash
set -euo pipefail

echo "Docker containers:"
docker ps --format '{{.Names}} {{.Image}}'
DB_CONTAINER=$(docker ps --format '{{.Names}}' | grep -E 'sila-db|sila_db|postgres' | head -n1 || true)
if [ -z "$DB_CONTAINER" ]; then
  echo "NO_DB_CONTAINER_FOUND"
  exit 0
fi

echo "Using DB container: $DB_CONTAINER"

TABLES=(locations territories territory_closure educacao_escolas educacao_turmas educacao_matriculas educacao_academic_identities educacao_boletins educacao_certificados educacao_institution_capacities)

for t in "${TABLES[@]}"; do
  echo
  echo "=== $t ==="
  docker exec -i "$DB_CONTAINER" psql -U sila_user -d sila_db -Atc "SELECT to_regclass('public.' || '${t}');" || true
  EXISTS=$(docker exec -i "$DB_CONTAINER" psql -U sila_user -d sila_db -Atc "SELECT to_regclass('public.' || '${t}');" || true)
  if [ -n "$EXISTS" ]; then
    echo "-- columns --"
    docker exec -i "$DB_CONTAINER" psql -U sila_user -d sila_db -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='public' AND table_name='${t}' ORDER BY ordinal_position;" || true
    echo "-- constraints --"
    docker exec -i "$DB_CONTAINER" psql -U sila_user -d sila_db -c "SELECT conname, pg_get_constraintdef(c.oid) FROM pg_constraint c JOIN pg_class t ON c.conrelid = t.oid WHERE t.relname = '${t}';" || true
  else
    echo "${t} DOES NOT EXIST"
  fi
done
