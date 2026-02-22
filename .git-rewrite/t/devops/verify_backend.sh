#!/bin/bash
# 🔍 Script de Verificação - Backend SILA
# Executa: bash devops/verify_backend.sh

echo "🔍 SILA Backend - Verificação de Saúde"
echo "======================================"
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}❌ $1${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# 1. Verificar containers rodando
echo "📦 Verificando containers..."
docker compose ps db | grep -q "Up" 2>/dev/null
check "Container db rodando"

docker compose ps backend | grep -q "Up" 2>/dev/null
check "Container backend rodando"

# 2. Verificar saúde do banco
echo ""
echo "🗄️  Verificando banco de dados..."
docker compose ps db | grep -q "healthy" 2>/dev/null
check "Banco de dados saudável"

BACKEND_CONTAINER="sila-backend"
docker exec $BACKEND_CONTAINER pg_isready -h db -U postgres > /dev/null 2>&1
check "Conexão com banco OK"

# 3. Verificar tabelas criadas
echo ""
echo "📊 Verificando estrutura do banco..."
TABLES=$(docker exec $(docker compose ps -q db) psql -U postgres -d sila -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | tr -d ' ')
if [ "$TABLES" -gt 0 ]; then
    echo -e "${GREEN}✅ $TABLES tabelas criadas${NC}"
    PASSED=$((PASSED + 1))
else
    echo -e "${RED}❌ Nenhuma tabela encontrada${NC}"
    FAILED=$((FAILED + 1))
fi

# 4. Verificar usuários criados
echo ""
echo "👤 Verificando usuários..."
USERS=$(docker exec $(docker compose ps -q db) psql -U postgres -d sila -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | tr -d ' ')
if [ "$USERS" -gt 0 ]; then
    echo -e "${GREEN}✅ $USERS usuários criados${NC}"
    PASSED=$((PASSED + 1))

    # Listar usuários
    echo ""
    echo "Usuários cadastrados:"
    docker exec $(docker compose ps -q db) psql -U postgres -d sila -c "SELECT username, email, role FROM users;" 2>/dev/null
else
    echo -e "${YELLOW}⚠️  Nenhum usuário encontrado${NC}"
fi

# 5. Verificar API
echo ""
echo "🌐 Verificando API..."
curl -s http://localhost:8000/health > /dev/null 2>&1
check "Endpoint /health respondendo"

curl -s http://localhost:8000/docs > /dev/null 2>&1
check "Endpoint /docs respondendo"

# 6. Verificar logs
echo ""
echo "📝 Últimas linhas do log do backend:"
docker compose logs --tail 10 backend

# Resumo
echo ""
echo "======================================"
echo "📊 RESUMO DA VERIFICAÇÃO"
echo "======================================"
echo -e "${GREEN}✅ Passou: $PASSED${NC}"
echo -e "${RED}❌ Falhou: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 Todos os testes passaram!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Alguns testes falharam. Revise os logs acima.${NC}"
    exit 1
fi
