#!/bin/bash
# Script para executar migrações e seeds do IAM + Citizen + Service Requests

echo "========================================"
echo "🚀 IAM + CITIZEN + SERVICE REQUESTS INTEGRATION SETUP"
echo "========================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# DATABASE_URL deve ser definido no ambiente (NÃO hardcoded)
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}❌ DATABASE_URL não definida no ambiente${NC}"
    echo -e "${YELLOW}Exemplo: export DATABASE_URL=\"postgresql://user:pass@host:5432/dbname\"${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Using DATABASE_URL from environment${NC}"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "alembic_core/alembic.ini" ]; then
    echo -e "${RED}❌ alembic_core/alembic.ini não encontrado. Execute este script a partir da pasta apps/backend${NC}"
    exit 1
fi

# Set PYTHONPATH to ensure modules are discoverable
export PYTHONPATH="${PYTHONPATH:-.}"

# 1. Executar migration usando alembic_core (o conjunto autoritativo de migrations)
echo -e "${YELLOW}📊 Executando migrations via alembic_core...${NC}"
python -m alembic -c alembic_core/alembic.ini upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migrations concluídas${NC}"
else
    echo -e "${RED}❌ Erro nas migrations${NC}"
    exit 1
fi

echo ""

# 2. Seed roles de cidadão (se script existir)
if [ -f "scripts/seed_citizen_roles.py" ]; then
    echo -e "${YELLOW}🌱 Criando roles e permissões para cidadãos...${NC}"
    python scripts/seed_citizen_roles.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Seeds de cidadão concluídos${NC}"
    else
        echo -e "${RED}❌ Erro nos seeds de cidadão (continuando de qualquer forma)${NC}"
    fi
fi

echo ""

# 3. Perguntar se quer criar cidadão de teste
read -p "❓ Criar cidadão de teste? (s/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    if [ -f "scripts/create_test_citizen.py" ]; then
        echo -e "${YELLOW}👤 Criando cidadão de teste...${NC}"
        python scripts/create_test_citizen.py
    else
        echo -e "${YELLOW}⚠️  scripts/create_test_citizen.py não encontrado${NC}"
    fi
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ INTEGRAÇÃO CONCLUÍDA!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "📚 Endpoints disponíveis:"
echo -e "  POST  /api/citizen/login     - Login de cidadão"
echo -e "  POST  /api/citizen/register  - Registrar conta"
echo -e "  POST  /api/citizen/link      - Vincular conta existente"
echo -e "  GET   /api/citizen/profile   - Perfil completo"
echo -e "  POST  /api/v1/service-requests/             - Criar solicitação"
echo -e "  GET   /api/v1/service-requests/{id}        - Obter solicitação"
echo -e ""

