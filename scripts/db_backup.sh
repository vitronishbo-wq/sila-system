#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

source "$SCRIPT_DIR/db_compose_env.sh"

DATE="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$ROOT_DIR/backups"
FILE="$BACKUP_DIR/full_$DATE.sql"
DB_USER="${POSTGRES_USER:-sila_user}"
DB_NAME="${POSTGRES_DB:-sila_db}"

mkdir -p "$BACKUP_DIR"
wait_for_db_ready

"${COMPOSE_CMD[@]}" exec -T db pg_dump --clean --if-exists -U "$DB_USER" "$DB_NAME" > "$FILE"
ln -sfn "$(basename "$FILE")" "$BACKUP_DIR/latest.sql"

echo "✅ Backup criado: $FILE"
echo "🔗 Latest atualizado: $BACKUP_DIR/latest.sql"
