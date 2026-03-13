#!/bin/bash
# 🗄️ Acesso Direto ao PostgreSQL (Local - Sem Docker)
# Conecta-se ao banco de dados sila_db com privilégios completos

set -e

# --- VARIÁVEIS ---
DB_USER="${POSTGRES_USER:-sila_user}"
DB_PASSWORD="${POSTGRES_PASSWORD:-Trumanmarcelo_1983}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-sila_db}"

echo "🔓 Conectando ao PostgreSQL..."
echo "   Host: $DB_HOST:$DB_PORT"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"
echo ""

# Exporta a senha para evitar prompt interativo
export PGPASSWORD="$DB_PASSWORD"

# Conecta ao banco
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"

# Limpa a variável de senha
unset PGPASSWORD
