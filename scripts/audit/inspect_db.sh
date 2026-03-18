#!/bin/bash
# 📊 Inspecionar Banco de Dados (Sem Docker)
# Valida a estrutura das províncias e conta registros

set -e

DB_USER="${POSTGRES_USER:-sila_user}"
DB_PASSWORD="${POSTGRES_PASSWORD:-Trumanmarcelo_1983}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-sila_db}"

export PGPASSWORD="$DB_PASSWORD"

echo "📊 === INSPEÇÃO DO BANCO DE DADOS ==="
echo ""

# Verifica conexão
echo "🔌 Testando conexão..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT version();" > /dev/null 2>&1 && echo "✅ Conexão OK" || echo "❌ Erro de conexão"
echo ""

# Conta províncias
echo "🌍 Total de Províncias (Lei 14/24):"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM locations WHERE type = 'PROVINCIA' AND parent_id IS NULL;" | xargs echo "   Províncias: "
echo ""

# Lista províncias
echo "📋 Províncias Cadastradas:"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT id, name FROM locations WHERE type = 'PROVINCIA' ORDER BY id;" | sed 's/^/   /'
echo ""

# Conta municípios
echo "🏙️ Total de Municípios:"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM locations WHERE type = 'MUNICIPIO';" | xargs echo "   Municípios: "
echo ""

# Conta comunas
echo "🏘️ Total de Comunas:"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT COUNT(*) FROM locations WHERE type = 'COMUNA';" | xargs echo "   Comunas: "
echo ""

# Estrutura da tabela
echo "🔍 Estrutura da Tabela 'locations':"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -t -c "\d locations" | sed 's/^/   /'

unset PGPASSWORD

echo ""
echo "✅ Inspeção concluída!"
