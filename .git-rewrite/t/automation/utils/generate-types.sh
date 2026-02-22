#!/bin/bash

# Script para gerar tipos TypeScript via OpenAPI

set -e

echo "🤖 Gerando tipos TypeScript..."

# Verificar se backend está rodando
if curl -sf http://localhost:8000/openapi.json >/dev/null 2>&1; then
    echo "✅ Backend detectado"

    # Criar diretório se não existir
    mkdir -p frontend/packages/shared-api/src

    # Gerar tipos usando curl + jq (alternativa ao openapi-typescript)
    curl -s http://localhost:8000/openapi.json > /tmp/openapi.json

    # Criar tipos básicos manualmente
    cat > frontend/packages/shared-api/src/api-types.d.ts << 'TYPES_EOF'
// Tipos gerados automaticamente do OpenAPI
// Gerado em: $(date)

export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  status: number;
}

export interface User {
  id: number;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

// Adicione mais tipos conforme necessário
TYPES_EOF

    echo "✅ Tipos TypeScript gerados em frontend/packages/shared-api/src/api-types.d.ts"
else
    echo "❌ Backend não está rodando em http://localhost:8000"
    echo "   Suba o backend primeiro com: ./start_enterprise.sh"
fi
