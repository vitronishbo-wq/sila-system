#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/db_compose_env.sh"

FILE="${1:-$ROOT_DIR/backups/latest.sql}"

if [[ ! -f "$FILE" ]]; then
    if [[ -f "$ROOT_DIR/$FILE" ]]; then
        FILE="$ROOT_DIR/$FILE"
    else
        echo "❌ Backup não encontrado: $FILE" >&2
        exit 1
    fi
fi

CONTAINER_ID="$(db_container_id || true)"
if [[ -z "$CONTAINER_ID" ]]; then
    "${COMPOSE_CMD[@]}" up -d db >/dev/null
    CONTAINER_ID="$(db_container_id)"
fi

DB_VOLUME="$(db_data_volume_name "$CONTAINER_ID")"
if [[ -z "$DB_VOLUME" ]]; then
    echo "❌ Não foi possível identificar o volume de dados do PostgreSQL." >&2
    exit 1
fi

docker rm -f "$CONTAINER_ID" >/dev/null 2>&1 || true
docker volume rm -f "$DB_VOLUME" >/dev/null 2>&1 || true

echo "🔄 Banco resetado. Subindo uma instância limpa..."
"${COMPOSE_CMD[@]}" up -d db
wait_for_db_ready

bash "$SCRIPT_DIR/db_restore.sh" "$FILE"

echo "✅ Reset completo concluído com restore: $FILE"
