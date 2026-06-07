#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/db_compose_env.sh"

FILE="${1:-}"
DB_USER="${POSTGRES_USER:-sila_user}"
DB_NAME="${POSTGRES_DB:-sila_db}"

if [[ -z "$FILE" ]]; then
    echo "❌ Uso: bash scripts/db_restore.sh backups/file.sql" >&2
    exit 1
fi

if [[ ! -f "$FILE" ]]; then
    if [[ -f "$ROOT_DIR/$FILE" ]]; then
        FILE="$ROOT_DIR/$FILE"
    else
        echo "❌ Backup não encontrado: $FILE" >&2
        exit 1
    fi
fi

wait_for_db_ready

"${COMPOSE_CMD[@]}" exec -T db psql -v ON_ERROR_STOP=1 -U "$DB_USER" "$DB_NAME" < "$FILE"

echo "✅ Restore concluído: $FILE"
