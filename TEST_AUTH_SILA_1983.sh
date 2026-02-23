#!/bin/bash

# Script para testar autenticação com senha Sila_1983
# Executa testes rápidos contra endpoint /api/auth/login

echo "================================"
echo "🔐 TESTE: Autenticação Sila_1983"
echo "================================"
echo ""

# Base URL (ajuste conforme necessário)
BASE_URL="http://localhost:8000"
AUTH_ENDPOINT="/api/auth/login"

# Array de usuários para testar
USERS=(
    "central@sila.gov.ao"
    "prov.huambo@sila.gov.ao"
    "mun.huambo@sila.gov.ao"
    "comun.huambo@sila.gov.ao"
    "truman@gmail.com"
)

# Função para testar login
test_login() {
    local email=$1
    local password="Sila_1983"
    
    echo -n "Testando $email... "
    
    # Fazer requisição POST para login
    response=$(curl -s -X POST "$BASE_URL$AUTH_ENDPOINT" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$email\", \"password\": \"$password\"}" \
        -w "\n%{http_code}")
    
    # Extrair status code (última linha)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" = "200" ]; then
        echo "✅ SUCCESS (HTTP 200)"
        # Extrair token se disponível
        token=$(echo "$body" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4 | head -1)
        if [ -n "$token" ]; then
            echo "  Token obtido: ${token:0:30}..."
        fi
    else
        echo "❌ FAILED (HTTP $http_code)"
        echo "  Resposta: $body"
    fi
    echo ""
}

echo "Testando cada usuário com senha: Sila_1983"
echo "Endpoint: $BASE_URL$AUTH_ENDPOINT"
echo ""

for user in "${USERS[@]}"; do
    test_login "$user"
done

echo "================================"
echo "✅ Teste de autenticação concluído"
echo "================================"
echo ""
echo "Próximos passos:"
echo "1. Verifique se todos os 5 usuários retornam HTTP 200"
echo "2. Se houver falhas, verifique logs do backend: docker logs sila-backend"
echo "3. Confirme que a senha Sila_1983 está sendo usada corretamente"
echo ""
