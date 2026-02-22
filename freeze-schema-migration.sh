#!/bin/bash
# ========================================
# SILA System - Production Schema Freeze
# Gera migração final e aplica ao banco
# ========================================

set -e

echo "🇦🇴 SILA System - Congelamento de Schema de Produção"
echo "=========================================="

# Verificar se backend está rodando
if ! docker compose ps backend | grep -q "Up"; then
    echo "❌ Backend não está rodando. Inicie com: docker compose up -d"
    exit 1
fi

echo "📊 Gerando migração automática..."

# Gerar migração automática
docker compose exec backend alembic revision --autogenerate -m "freeze_production_schema_v1"

echo ""
echo "✅ Migração gerada!"
echo ""
echo "📝 IMPORTANTE: Verifique o arquivo de migração gerado em:"
echo "   apps/backend/migrations/versions/"
echo ""
echo "   Certifique-se de que contém:"
echo "   - Coluna search_vector (TSVECTOR)"
echo "   - Índice GIN (idx_documents_search)"
echo "   - Trigger de atualização automática"
echo ""

read -p "Deseja aplicar a migração agora? (s/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🔄 Aplicando migração..."
    docker compose exec backend alembic upgrade head
    
    echo ""
    echo "✅ Migração aplicada com sucesso!"
    echo ""
    
    # Verificar índices criados
    echo "📋 Verificando índices no banco de dados..."
    docker compose exec db psql -U sila_user -d sila -c "\di" | grep -E "(idx_documents_search|idx_audit)"
    
    echo ""
    echo "=========================================="
    echo "✅ Schema de produção congelado!"
    echo ""
    echo "📋 Próximos passos:"
    echo "   1. Testar login: admin@sila.gov.ao / Admin123!"
    echo "   2. Verificar audit logs"
    echo "   3. Testar upload de documento"
    echo "   4. Testar busca profunda (Ctrl+K)"
    echo "=========================================="
else
    echo "⏸️  Migração não aplicada. Execute manualmente quando estiver pronto:"
    echo "   docker compose exec backend alembic upgrade head"
fi
