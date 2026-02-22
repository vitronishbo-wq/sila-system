#!/bin/bash
# Teste final completo das correções
cd "$(dirname "$0")"

export COMPOSE_FILE="docker-compose.yml"
export COMPOSE_PROJECT_NAME="sila-devops"

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "🧪 TESTE FINAL - Validação de Correções"
echo "=========================================="
echo ""

ERRORS=0

# Teste 1: YAML válido
echo -e "${BLUE}Teste 1: Validação do YAML${NC}"
if docker compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✅ YAML válido${NC}"
else
    echo -e "${RED}❌ YAML inválido${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 2: Profiles existem
echo -e "${BLUE}Teste 2: Profiles configurados${NC}"
PROFILES=$(docker compose config --profiles 2>/dev/null)
if echo "$PROFILES" | grep -q "infra" && echo "$PROFILES" | grep -q "backend"; then
    echo -e "${GREEN}✅ Profiles 'infra' e 'backend' encontrados${NC}"
    echo "   Profiles: $(echo $PROFILES | tr '\n' ', ')"
else
    echo -e "${RED}❌ Profiles não encontrados${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 3: Serviços com profiles ativos
echo -e "${BLUE}Teste 3: Serviços com profiles ativos${NC}"
SERVICES=$(docker compose --profile infra --profile backend config --services 2>/dev/null)
if echo "$SERVICES" | grep -q "db" && echo "$SERVICES" | grep -q "backend"; then
    echo -e "${GREEN}✅ Serviços 'db' e 'backend' disponíveis${NC}"
    echo "   Serviços: $(echo $SERVICES | tr '\n' ', ')"
else
    echo -e "${RED}❌ Serviços não encontrados${NC}"
    echo "   Encontrados: $SERVICES"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 4: Configuração compilada
echo -e "${BLUE}Teste 4: Configuração compilada (com profiles)${NC}"
CONFIG=$(docker compose --profile infra --profile backend config 2>&1)
if echo "$CONFIG" | grep -q "sila-db" && echo "$CONFIG" | grep -q "sila-backend"; then
    echo -e "${GREEN}✅ Containers 'sila-db' e 'sila-backend' na configuração${NC}"
else
    echo -e "${RED}❌ Containers não encontrados na configuração${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 5: Dependências
echo -e "${BLUE}Teste 5: Verificação de dependências${NC}"
if echo "$CONFIG" | grep -A10 "sila-backend" | grep -q "depends_on"; then
    echo -e "${GREEN}✅ Backend tem dependências configuradas${NC}"
    if echo "$CONFIG" | grep -A10 "depends_on" | grep -q "db:"; then
        echo -e "${GREEN}✅ Backend depende de 'db'${NC}"
    else
        echo -e "${RED}❌ Dependência 'db' não encontrada${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ Nenhuma dependência encontrada${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 6: Networks
echo -e "${BLUE}Teste 6: Networks configuradas${NC}"
if echo "$CONFIG" | grep -q "app-network" && echo "$CONFIG" | grep -q "monitoring"; then
    echo -e "${GREEN}✅ Networks 'app-network' e 'monitoring' configuradas${NC}"
else
    echo -e "${RED}❌ Networks não configuradas corretamente${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 7: Volumes
echo -e "${BLUE}Teste 7: Volumes configurados${NC}"
if echo "$CONFIG" | grep -q "postgres_data" && echo "$CONFIG" | grep -q "prometheus_data"; then
    echo -e "${GREEN}✅ Volumes 'postgres_data' e 'prometheus_data' configurados${NC}"
else
    echo -e "${RED}❌ Volumes não configurados${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 8: Healthcheck do DB
echo -e "${BLUE}Teste 8: Healthcheck do PostgreSQL${NC}"
if echo "$CONFIG" | grep -A5 "sila-db" | grep -q "healthcheck"; then
    echo -e "${GREEN}✅ Healthcheck configurado para DB${NC}"
else
    echo -e "${RED}❌ Healthcheck não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Teste 9: Portas
echo -e "${BLUE}Teste 9: Mapeamento de portas${NC}"
DB_PORT=$(echo "$CONFIG" | grep -o "5434:5432" || echo "")
BACKEND_PORT=$(echo "$CONFIG" | grep -o "8000:8000" || echo "")
if [ -n "$DB_PORT" ] && [ -n "$BACKEND_PORT" ]; then
    echo -e "${GREEN}✅ Portas 5434 (DB) e 8000 (Backend) mapeadas${NC}"
elif [ -n "$DB_PORT" ] || [ -n "$BACKEND_PORT" ]; then
    echo -e "${GREEN}✅ Portas configuradas (DB: $DB_PORT, Backend: $BACKEND_PORT)${NC}"
else
    # Verificar formato alternativo
    if echo "$CONFIG" | grep -q "published.*5434" && echo "$CONFIG" | grep -q "published.*8000"; then
        echo -e "${GREEN}✅ Portas configuradas (formato longo)${NC}"
    else
        echo -e "${RED}❌ Portas não mapeadas corretamente${NC}"
        ERRORS=$((ERRORS + 1))
    fi
fi
echo ""

# Teste 10: Entrypoint existe
echo -e "${BLUE}Teste 10: Arquivo entrypoint.sh${NC}"
if [ -f "../backend/entrypoint.sh" ]; then
    echo -e "${GREEN}✅ entrypoint.sh existe${NC}"
    if grep -q "exec uvicorn" "../backend/entrypoint.sh"; then
        echo -e "${GREEN}✅ entrypoint.sh usa 'exec uvicorn' (correção aplicada)${NC}"
    else
        echo -e "${RED}❌ entrypoint.sh não usa 'exec uvicorn'${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${RED}❌ entrypoint.sh não encontrado${NC}"
    ERRORS=$((ERRORS + 1))
fi
echo ""

# Resultado Final
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ TODOS OS TESTES PASSARAM!${NC}"
    echo -e "${GREEN}✅ Correções validadas com sucesso${NC}"
    echo "=========================================="
    echo ""
    echo "Próximo passo:"
    echo "  bash start_backend.sh"
    exit 0
else
    echo -e "${RED}❌ $ERRORS TESTE(S) FALHARAM${NC}"
    echo "=========================================="
    exit 1
fi
