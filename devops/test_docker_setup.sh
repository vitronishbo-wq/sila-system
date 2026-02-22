#!/bin/bash
# devops/test_docker_setup.sh
# Script de teste para validar configuração Docker Compose

set -euo pipefail

# Cores para output legível
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error()   { echo -e "${RED}❌ $1${NC}"; }

# Garante que o script rode a partir do diretório onde está localizado
cd "$(dirname "$0")"

# Configuração de contexto para o teste
export COMPOSE_FILE="../docker-compose.yml"
export COMPOSE_PROJECT_NAME="sila-devops"

echo "=========================================="
echo "🧪 Teste de Configuração Docker Compose"
echo "=========================================="
echo ""

# Teste 1: Validar YAML
log_info "Teste 1: Validando sintaxe do docker-compose.yml..."
if docker compose config > /dev/null 2>&1; then
    log_success "YAML válido"
else
    log_error "YAML inválido"
    docker compose config
    exit 1
fi

# Teste 2: Listar serviços
log_info "Teste 2: Listando serviços disponíveis..."
SERVICES=$(docker compose config --services 2>/dev/null || echo "")
if [ -n "$SERVICES" ]; then
    echo "$SERVICES" | while read -r service; do
        echo "   - $service"
    done
    log_success "Serviços listados"
else
    log_error "Nenhum serviço encontrado"
    exit 1
fi

# Teste 5: Verificar networks
log_info "Teste 5: Verificando networks..."
if docker compose config | grep -q "networks:"; then
    log_success "Networks configuradas"
else
    log_error "Nenhuma network encontrada"
    exit 1
fi

# Teste 9: Verificar Dockerfiles (Caminhos relativos ao script)
log_info "Teste 9: Verificando Dockerfiles..."
if [ -f "../apps/backend/Dockerfile" ]; then
    log_success "backend/Dockerfile existe"
else
    log_error "backend/Dockerfile não encontrado em ../apps/backend/Dockerfile"
    exit 1
fi

if [ -f "../apps/frontend/Dockerfile" ]; then
    log_success "frontend/Dockerfile existe"
else
    log_warning "frontend/Dockerfile não encontrado"
fi

# Teste 10: Verificar entrypoint e permissões
log_info "Teste 10: Verificando entrypoint.sh..."
ENTRYPOINT_PATH="../apps/backend/entrypoint.sh"
if [ -f "$ENTRYPOINT_PATH" ]; then
    if [ -x "$ENTRYPOINT_PATH" ]; then
        log_success "backend/entrypoint.sh existe e é executável"
    else
        log_warning "backend/entrypoint.sh existe mas não é executável"
        chmod +x "$ENTRYPOINT_PATH"
        log_success "Permissão de execução adicionada automaticamente"
    fi
else
    log_error "backend/entrypoint.sh não encontrado"
    exit 1
fi

# Teste 13: Simular configuração compilada e nomes de containers
log_info "Teste 13: Gerando configuração compilada..."
COMPILED_CONFIG=$(docker compose config 2>&1)
if echo "$COMPILED_CONFIG" | grep -q "services:"; then
    log_success "Configuração compilada com sucesso"

    if echo "$COMPILED_CONFIG" | grep -q "sila-db"; then
        log_success "Serviço 'db' (sila-db) presente na configuração"
    else
        log_error "Serviço 'db' NÃO encontrado na configuração"
        exit 1
    fi
else
    log_error "Falha ao compilar configuração"
    echo "$COMPILED_CONFIG"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Todos os testes de infraestrutura passaram!${NC}"
echo "=========================================="