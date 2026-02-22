#!/bin/bash
# ========================================
# SILA System - Database Schema Freeze
# Gera snapshot do schema atual para produção
# ========================================

set -e

echo "🇦🇴 SILA System - Congelamento de Schema para Produção"
echo "=========================================="

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
SCHEMA_FILE="schema_freeze_${TIMESTAMP}.sql"

echo "📊 Gerando snapshot do schema atual..."

# Exportar schema completo (sem dados)
docker exec -t sila-db pg_dump \
    -U sila_user \
    -d sila \
    --schema-only \
    --no-owner \
    --no-privileges \
    > "./backups/${SCHEMA_FILE}"

echo "✅ Schema exportado: backups/${SCHEMA_FILE}"

# Criar versão limpa (sem comentários de dump)
grep -v "^--" "./backups/${SCHEMA_FILE}" | \
grep -v "^$" | \
grep -v "^SET" | \
grep -v "^SELECT pg_catalog" \
> "./backups/schema_production.sql"

echo "✅ Schema limpo criado: backups/schema_production.sql"

# Gerar relatório de tabelas
echo ""
echo "📋 Tabelas no Schema:"
docker exec -t sila-db psql -U sila_user -d sila -c "\dt" | grep "public"

echo ""
echo "📋 Índices Criados:"
docker exec -t sila-db psql -U sila_user -d sila -c "\di" | grep "public" | head -20

echo ""
echo "=========================================="
echo "✅ Schema congelado com sucesso!"
echo ""
echo "📁 Arquivos gerados:"
echo "   - backups/${SCHEMA_FILE} (completo)"
echo "   - backups/schema_production.sql (limpo)"
echo ""
echo "🚀 Para aplicar em produção:"
echo "   psql -U sila_user -d sila_prod < backups/schema_production.sql"
echo "=========================================="
