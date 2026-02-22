#!/bin/bash

# Cores para o output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔍 Iniciando testes de integridade do SILA-System...${NC}"

# 1. Testar Healthcheck da API
echo -n "1. Verificando Healthcheck da API... "
HEALTH=$(curl -s http://localhost:8000/health | grep -o "healthy")
if [ "$HEALTH" == "healthy" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FALHA (Verifica se o container backend está rodando)${NC}"
fi

# 2. Testar Login do Administrador Inicial (Credenciais do setup_admin.py)
echo -n "2. Testando login do administrador (JWT)... "
# Ajustado para usar a password 'admin123' que definimos no script de setup
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@sila.gov.ao&password=admin123")

TOKEN=$(echo $LOGIN_RESPONSE | grep -oP '(?<="access_token":")[^"]*')

if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}SUCESSO${NC}"
    echo -e "   Token gerado: ${TOKEN:0:20}..."
else
    echo -e "${RED}FALHA${NC}"
    echo -e "   Resposta: $LOGIN_RESPONSE"
fi

# 3. Testar Acesso Protegido (Identity Module)
echo -n "3. Verificando acesso ao módulo Identity... "
USER_INFO=$(curl -s -X GET "http://localhost:8000/api/v1/identity/me" \
     -H "Authorization: Bearer $TOKEN")

if [[ "$USER_INFO" == *"admin@sila.gov.ao"* ]]; then
    echo -e "${GREEN}CONSOLIDADO${NC}"
else
    echo -e "${RED}FALHA (Erro de permissão ou modelo)${NC}"
    echo -e "   Resposta: $USER_INFO"
fi

echo -e "\n${GREEN}🚀 Testes concluídos!${NC}"