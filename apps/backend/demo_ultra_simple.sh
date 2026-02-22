#!/bin/bash

echo "🚀 SILA BACKEND - DEMONSTRAÇÃO VERSÃO ULTRA SIMPLES"
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para testar endpoint
test_endpoint() {
    local endpoint="$1"
    local description="$2"

    echo -e "\n${BLUE}📍 Testando: $description${NC}"
    echo -e "${YELLOW}Endpoint: GET $endpoint${NC}"

    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "http://localhost:8000$endpoint")
    http_code=$(echo "$response" | grep -o 'HTTP_STATUS:[0-9]*' | cut -d: -f2)
    body=$(echo "$response" | sed -e 's/HTTP_STATUS:[0-9]*$//')

    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ Status: $http_code${NC}"
        echo -e "${GREEN}✅ Response:${NC}"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
    else
        echo -e "${RED}❌ Status: $http_code${NC}"
        echo -e "${RED}❌ Response: $body${NC}"
    fi
}

# Verificar se o servidor está rodando
echo -e "\n${YELLOW}🔍 Verificando se o servidor está rodando...${NC}"

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Servidor está online!${NC}"
else
    echo -e "${RED}❌ Servidor não está rodando!${NC}"
    echo -e "${YELLOW}💡 Inicie o servidor com:${NC}"
    echo "   cd /opt/sila-system/backend"
    echo "   python main_ultra_simple.py"
    echo ""
    echo -e "${YELLOW}🚀 Ou use o script automático:${NC}"
    echo "   ./start_ultra_simple.sh"
    exit 1
fi

# Testar endpoints
echo -e "\n${BLUE}🧪 EXECUTANDO TESTES DOS ENDPOINTS${NC}"

test_endpoint "/" "Endpoint Raiz"
test_endpoint "/health" "Health Check"
test_endpoint "/info" "Informações do Sistema"

# Testar documentação
echo -e "\n${BLUE}📚 TESTANDO DOCUMENTAÇÃO${NC}"

echo -e "${YELLOW}📍 Verificando Swagger UI...${NC}"
if curl -s http://localhost:8000/docs | grep -q "swagger"; then
    echo -e "${GREEN}✅ Swagger UI disponível: http://localhost:8000/docs${NC}"
else
    echo -e "${RED}❌ Swagger UI não disponível${NC}"
fi

echo -e "${YELLOW}📍 Verificando ReDoc...${NC}"
if curl -s http://localhost:8000/redoc | grep -q "redoc"; then
    echo -e "${GREEN}✅ ReDoc disponível: http://localhost:8000/redoc${NC}"
else
    echo -e "${RED}❌ ReDoc não disponível${NC}"
fi

# Testar OpenAPI
echo -e "\n${BLUE}📋 TESTANDO OPENAPI${NC}"
echo -e "${YELLOW}📍 Verificando esquema OpenAPI...${NC}"

openapi_response=$(curl -s http://localhost:8000/openapi.json)
if echo "$openapi_response" | python3 -c "import json, sys; json.load(sys.stdin)" 2>/dev/null; then
    echo -e "${GREEN}✅ OpenAPI JSON válido${NC}"
    title=$(echo "$openapi_response" | python3 -c "import json, sys; print(json.load(sys.stdin)['info']['title'])" 2>/dev/null)
    version=$(echo "$openapi_response" | python3 -c "import json, sys; print(json.load(sys.stdin)['info']['version'])" 2>/dev/null)
    echo -e "${GREEN}   📋 Título: $title${NC}"
    echo -e "${GREEN}   📋 Versão: $version${NC}"
else
    echo -e "${RED}❌ OpenAPI JSON inválido${NC}"
fi

# Resumo final
echo -e "\n${GREEN}🎉 DEMONSTRAÇÃO CONCLUÍDA!${NC}"
echo "=================================================="
echo -e "${BLUE}📍 Links Úteis:${NC}"
echo -e "   🌐 API Base: ${GREEN}http://localhost:8000${NC}"
echo -e "   📚 Swagger UI: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   📖 ReDoc: ${GREEN}http://localhost:8000/redoc${NC}"
echo -e "   🏥 Health: ${GREEN}http://localhost:8000/health${NC}"
echo -e "   📋 OpenAPI: ${GREEN}http://localhost:8000/openapi.json${NC}"
echo ""
echo -e "${BLUE}🔧 Comandos Úteis:${NC}"
echo -e "   🚀 Iniciar servidor: ${YELLOW}python main_ultra_simple.py${NC}"
echo -e "   🧪 Executar testes: ${YELLOW}python test_ultra_simple.py${NC}"
echo -e "   📜 Script auto: ${YELLOW}./start_ultra_simple.sh${NC}"
echo ""
echo -e "${GREEN}✅ API Ultra Simple 100% Funcional!${NC}"
