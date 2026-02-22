#!/bin/bash

BASE_URL="http://localhost:8000/api/v1/auth"

echo "🔍 Verificando Login Central..."

# Function to test login
test_login() {
    EMAIL=$1
    PASSWORD=$2
    LABEL=$3

    echo ""
    echo "🔵 Teste: $LABEL ($EMAIL)"
    
    RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

    # Check if access token is present
    if echo "$RESPONSE" | grep -q "access"; then
        echo "   ✅ Login bem-sucedido!"
        TOKEN=$(echo "$RESPONSE" | grep -o '"access":"[^"]*' | grep -o '[^"]*$')
        echo "   🔑 Token obtido"
        
        # Test /me
        ME_RESPONSE=$(curl -s -X GET "$BASE_URL/me" \
            -H "Authorization: Bearer $TOKEN")
        
        if echo "$ME_RESPONSE" | grep -q "email"; then
            echo "   👤 Usuário verificado via /me"
            echo "   Dados: $ME_RESPONSE"
        else
            echo "   ❌ Falha em /me: $ME_RESPONSE"
        fi
    else
        echo "   ❌ Login Falhou"
        echo "   Resposta: $RESPONSE"
    fi
}

test_login "admin_central_central@sila.gov.ao" "admin123" "Central User (Seed)"
test_login "admin@sila.gov.ao" "admin123" "Admin Bootstrap"
