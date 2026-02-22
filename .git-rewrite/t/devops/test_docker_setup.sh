#!/bin/bash
# devops/test_docker_setup.sh
# Script de teste para validar configuração Docker Compose

set -euo pipefail

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error()   { echo -e "${RED}❌ $1${NC}"; }

cd "$(dirname "$0")"

# Forçar uso do docker-compose.yml local
export COMPOSE_FILE="docker-compose.yml"
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
        echo "  - $service"
    done
    log_success "Serviços listados"
else
    log_error "Nenhum serviço encontrado"
    exit 1
fi

# Teste 3: Verificar profiles
log_info "Teste 3: Verificando profiles..."
PROFILES=$(docker compose config --profiles 2>/dev/null || echo "")
if [ -n "$PROFILES" ]; then
    echo "$PROFILES" | while read -r profile; do
        echo "  - $profile"
    done
    log_success "Profiles encontrados"
else
    log_warning "Nenhum profile definido"
fi

# Teste 4: Verificar dependências
log_info "Teste 4: Verificando dependências entre serviços..."
if docker compose config | grep -q "depends_on"; then
    log_success "Dependências configuradas"
else
    log_warning "Nenhuma dependência encontrada"
fi

# Teste 5: Verificar networks
log_info "Teste 5: Verificando networks..."
if docker compose config | grep -q "networks:"; then
    log_success "Networks configuradas"
else
    log_error "Nenhuma network encontrada"
    exit 1
fi

# Teste 6: Verificar volumes
log_info "Teste 6: Verificando volumes..."
if docker compose config | grep -q "volumes:"; then
    log_success "Volumes configurados"
else
    log_warning "Nenhum volume encontrado"
fi

# Teste 7: Verificar rede externa
log_info "Teste 7: Verificando rede sila-monitoring..."
if docker network inspect sila-monitoring > /dev/null 2>&1; then
    log_success "Rede sila-monitoring existe"
else
    log_warning "Rede sila-monitoring não existe (será criada automaticamente)"
fi

# Teste 8: Verificar imagens necessárias
log_info "Teste 8: Verificando imagens Docker..."
if docker images | grep -q "postgres"; then
    log_success "Imagem postgres encontrada"
else
    log_warning "Imagem postgres não encontrada (será baixada)"
fi

# Teste 9: Verificar Dockerfiles
log_info "Teste 9: Verificando Dockerfiles..."
if [ -f "../backend/Dockerfile" ]; then
    log_success "backend/Dockerfile existe"
else
    log_error "backend/Dockerfile não encontrado"
    exit 1
fi

if [ -f "../frontend/apps/web/Dockerfile" ]; then
    log_success "frontend/apps/web/Dockerfile existe"
else
    log_warning "frontend/apps/web/Dockerfile não encontrado"
fi

# Teste 10: Verificar entrypoint
log_info "Teste 10: Verificando entrypoint.sh..."
if [ -f "../backend/entrypoint.sh" ]; then
    if [ -x "../backend/entrypoint.sh" ]; then
        log_success "backend/entrypoint.sh existe e é executável"
    else
        log_warning "backend/entrypoint.sh existe mas não é executável"
        chmod +x ../backend/entrypoint.sh
        log_success "Permissão de execução adicionada"
    fi
else
    log_error "backend/entrypoint.sh não encontrado"
    exit 1
fi

# Teste 11: Verificar configuração Nginx
log_info "Teste 11: Verificando configuração Nginx..."
if [ -f "nginx/frontend.conf" ]; then
    log_success "nginx/frontend.conf existe"
else
    log_warning "nginx/frontend.conf não encontrado"
fi

# Teste 12: Verificar variáveis de ambiente
log_info "Teste 12: Verificando variáveis de ambiente..."
echo "  COMPOSE_FILE: ${COMPOSE_FILE:-não definido}"
echo "  COMPOSE_PROJECT_NAME: ${COMPOSE_PROJECT_NAME:-não definido}"

# Teste 13: Simular configuração compilada
log_info "Teste 13: Gerando configuração compilada..."
COMPILED_CONFIG=$(docker compose config 2>&1)
if echo "$COMPILED_CONFIG" | grep -q "services:"; then
    log_success "Configuração compilada com sucesso"

    # Verificar se db está presente
    if echo "$COMPILED_CONFIG" | grep -q "sila-db"; then
        log_success "Serviço 'db' presente na configuração"
    else
        log_error "Serviço 'db' NÃO encontrado na configuração"
        exit 1
    fi

    # Verificar se backend está presente
    if echo "$COMPILED_CONFIG" | grep -q "sila-backend"; then
        log_success "Serviço 'backend' presente na configuração"
    else
        log_error "Serviço 'backend' NÃO encontrado na configuração"
        exit 1
    fi
else
    log_error "Falha ao compilar configuração"
    echo "$COMPILED_CONFIG"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Todos os testes passaram!${NC}"
echo "=========================================="
echo ""
echo "Próximos passos:"
echo "  1. Executar: bash start_backend.sh"
echo "  2. Verificar: docker compose ps"
echo "  3. Testar API: curl http://localhost:8000/health"
echo ""
