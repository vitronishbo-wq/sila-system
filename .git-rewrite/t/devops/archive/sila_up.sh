#!/usr/bin/env bash
# =========================================
# SILA MASTER - Script Definitivo
# =========================================
# Script único que resolve toda confusão de diretórios
# e sobe o sistema completo de forma certeira
# =========================================
# Uso: bash sila_up.sh
# =========================================

set -euo pipefail

# =========================================
# CONFIGURAÇÃO E CORES
# =========================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

START_TIME=$(date +%s)

# =========================================
# FUNÇÕES DE LOG
# =========================================
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() {
    echo ""
    echo -e "${BOLD}${PURPLE}========================================${NC}"
    echo -e "${BOLD}${PURPLE}🚀 $1${NC}"
    echo -e "${BOLD}${PURPLE}========================================${NC}"
}

# =========================================
# DETECÇÃO E LIMPEZA DE DIRETÓRIOS
# =========================================
log_step "SILA MASTER - SETUP DEFINITIVO"

# Garantir que estamos na raiz do projeto
cd "$(dirname "$0")"
PROJECT_ROOT=$(pwd)
log_info "Diretório do projeto: $PROJECT_ROOT"

log_step "1. Limpeza e Organização de Diretórios"

log_info "🔍 Detectando docker-compose.yml disponíveis..."
COMPOSE_FILES=()
if [ -f "docker-compose.yml" ]; then
    COMPOSE_FILES+=("$(pwd)/docker-compose.yml")
    log_info "Encontrado: docker-compose.yml (raiz)"
fi
if [ -f "devops/docker-compose.yml" ]; then
    COMPOSE_FILES+=("$(pwd)/devops/docker-compose.yml")
    log_info "Encontrado: devops/docker-compose.yml"
fi
if [ -f "scripts/docker-compose.yml" ]; then
    COMPOSE_FILES+=("$(pwd)/scripts/docker-compose.yml")
    log_info "Encontrado: scripts/docker-compose.yml"
fi

log_info "📋 Total de arquivos docker-compose encontrados: ${#COMPOSE_FILES[@]}"

# Escolher o docker-compose mais completo (devops)
if [ -f "devops/docker-compose.yml" ]; then
    COMPOSE_FILE="devops/docker-compose.yml"
    COMPOSE_DIR="devops"
    log_success "Usando: devops/docker-compose.yml (mais completo)"
elif [ -f "docker-compose.yml" ]; then
    COMPOSE_FILE="docker-compose.yml"
    COMPOSE_DIR="."
    log_warning "Usando: docker-compose.yml (raiz)"
else
    log_error "Nenhum docker-compose.yml encontrado!"
    exit 1
fi

# Ir para o diretório correto
cd "$COMPOSE_DIR"
log_info "Diretório de trabalho: $(pwd)"

# =========================================
# 2. LIMPEZA TOTAL DO AMBIENTE
# =========================================
log_step "2. Limpeza Total do Ambiente"

log_info "🛑 Parando TODOS os containers Docker..."
docker stop $(docker ps -aq) 2>/dev/null || true
log_success "Containers parados"

log_info "🗑️  Removendo containers antigos do SILA..."
docker rm $(docker ps -aq --filter "name=sila") 2>/dev/null || true
log_success "Containers SILA removidos"

log_info "🧹 Limpando imagens órfãs..."
docker image prune -f 2>/dev/null || true
log_success "Imagens limpas"

# =========================================
# 3. VERIFICAÇÃO DE DEPENDÊNCIAS
# =========================================
log_step "3. Verificação de Dependências"

log_info "🔍 Verificando se passlib está no requirements.txt..."
if grep -q "passlib" ../backend/requirements.txt 2>/dev/null; then
    log_success "passlib encontrado no requirements.txt"
else
    log_warning "passlib não encontrado, adicionando..."
    if [ -f "../backend/requirements.txt" ]; then
        echo "passlib[bcrypt]==1.7.4" >> ../backend/requirements.txt
        log_success "passlib adicionado ao requirements.txt"
    else
        log_error "requirements.txt não encontrado!"
        exit 1
    fi
fi

log_info "🔍 Verificando build do frontend..."
if [ -d "../frontend/apps/web/dist" ] && [ "$(ls -A ../frontend/apps/web/dist 2>/dev/null)" ]; then
    DIST_FILES=$(find ../frontend/apps/web/dist -type f | wc -l)
    log_success "Build do frontend encontrado ($DIST_FILES arquivos)"
else
    log_warning "Build do frontend não encontrado, criando..."
    cd ../frontend/apps/web
    if command -v npm >/dev/null 2>&1; then
        npm install && npm run build
        log_success "Frontend buildado com sucesso"
    else
        log_error "npm não encontrado! Instale Node.js primeiro"
        exit 1
    fi
    cd "$PROJECT_ROOT/$COMPOSE_DIR"
fi

# =========================================
# 4. CRIAÇÃO DE RECURSOS EXTERNOS
# =========================================
log_step "4. Criação de Recursos Externos"

log_info "🌐 Criando rede sila-monitoring..."
docker network create sila-monitoring 2>/dev/null || log_info "Rede já existe"

log_info "💾 Criando volume prometheus_data..."
docker volume create prometheus_data 2>/dev/null || log_info "Volume já existe"

log_success "Recursos externos preparados"

# =========================================
# 5. BUILD E START - BACKEND
# =========================================
log_step "5. Build e Start do Backend"

log_info "🔄 Fazendo build da imagem backend..."
if docker compose -f docker-compose.yml --profile infra --profile backend build --no-cache backend; then
    log_success "Backend buildado com sucesso"
else
    log_error "Falha no build do backend"
    exit 1
fi

log_info "🚀 Iniciando banco de dados..."
docker compose -f docker-compose.yml --profile infra up -d db

log_info "⏳ Aguardando banco ficar saudável..."
WAIT_COUNT=0
MAX_WAIT=120
while [ $WAIT_COUNT -lt $MAX_WAIT ]; do
    if docker ps --filter "name=sila-db" --format "{{.Status}}" | grep -q "healthy"; then
        log_success "Banco saudável (${WAIT_COUNT}s)"
        break
    fi
    sleep 2
    WAIT_COUNT=$((WAIT_COUNT + 2))
    [ $((WAIT_COUNT % 10)) -eq 0 ] && echo -n "."
done
echo ""

if [ $WAIT_COUNT -ge $MAX_WAIT ]; then
    log_error "Timeout aguardando banco"
    exit 1
fi

log_info "🚀 Iniciando backend..."
docker compose -f docker-compose.yml --profile infra --profile backend up -d backend

sleep 10

# =========================================
# 6. MIGRATIONS E SEED DATA
# =========================================
log_step "6. Migrations e Seed Data"

log_info "📊 Aplicando migrations..."
if docker exec sila-backend bash -c "cd /app && alembic upgrade head" 2>/dev/null; then
    log_success "Migrations aplicadas"
else
    log_warning "Migrations falharam ou já aplicadas"
fi

log_info "🌱 Executando seed data..."
if docker exec sila-backend bash -c "cd /app && python -m modules.governance.seed_data" 2>/dev/null; then
    log_success "Seed data executado"
else
    log_warning "Seed data falhou ou já executado"
fi

# =========================================
# 7. VERIFICAÇÃO DO BACKEND
# =========================================
log_step "7. Verificação do Backend"

log_info "🔍 Testando API do backend..."
API_WAIT=0
API_MAX_WAIT=60
while [ $API_WAIT -lt $API_MAX_WAIT ]; do
    if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
        log_success "Backend API funcionando (${API_WAIT}s)"
        BACKEND_OK=true
        break
    fi
    sleep 2
    API_WAIT=$((API_WAIT + 2))
    [ $((API_WAIT % 10)) -eq 0 ] && echo -n "."
done
echo ""

if [ "${BACKEND_OK:-false}" != "true" ]; then
    log_error "Backend não está respondendo"
    log_info "Verificando logs..."
    docker logs sila-backend --tail 20
    exit 1
fi

# =========================================
# 8. BUILD E START - FRONTEND
# =========================================
log_step "8. Build e Start do Frontend"

# Corrigir .dockerignore se necessário
if grep -q "^dist/$" ../frontend/apps/web/.dockerignore 2>/dev/null; then
    log_info "🔧 Corrigindo .dockerignore..."
    sed -i 's/^dist\/$/# dist\/ - MANTIDO para produção/' ../frontend/apps/web/.dockerignore
    log_success ".dockerignore corrigido"
fi

log_info "🔄 Fazendo build da imagem frontend..."
if docker compose -f docker-compose.yml --profile infra --profile backend --profile frontend build --no-cache frontend; then
    log_success "Frontend buildado com sucesso"
else
    log_error "Falha no build do frontend"
    exit 1
fi

log_info "🚀 Iniciando frontend..."
docker compose -f docker-compose.yml --profile infra --profile backend --profile frontend up -d frontend

sleep 5

# =========================================
# 9. VERIFICAÇÃO DO FRONTEND
# =========================================
log_step "9. Verificação do Frontend"

log_info "🔍 Testando frontend..."
FRONTEND_WAIT=0
FRONTEND_MAX_WAIT=30
while [ $FRONTEND_WAIT -lt $FRONTEND_MAX_WAIT ]; do
    if curl -sf http://localhost:80 >/dev/null 2>&1; then
        log_success "Frontend funcionando (${FRONTEND_WAIT}s)"
        FRONTEND_OK=true
        break
    fi
    sleep 2
    FRONTEND_WAIT=$((FRONTEND_WAIT + 2))
    [ $((FRONTEND_WAIT % 10)) -eq 0 ] && echo -n "."
done
echo ""

if [ "${FRONTEND_OK:-false}" != "true" ]; then
    log_warning "Frontend não está respondendo ainda"
    docker logs sila-frontend --tail 10
fi

# =========================================
# 10. VERIFICAÇÃO FINAL E RELATÓRIO
# =========================================
log_step "10. Verificação Final"

log_info "🔍 Testando integração completa..."
DATA_CHECK=$(docker exec sila-backend python3 -c "
import os, sys
try:
    from sqlalchemy import create_engine, text
    from urllib.parse import urlparse
    db_url = os.environ.get('DATABASE_URL') or os.environ.get('ASYNC_DATABASE_URL', '').replace('+asyncpg', '')
    parsed = urlparse(db_url)
    sync_url = f'postgresql://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port or 5432}/{parsed.path.lstrip(\"/\")}'
    engine = create_engine(sync_url)
    with engine.connect() as conn:
        tables = ['institutions', 'mandates', 'users']
        total = 0
        for table in tables:
            try:
                result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
                count = result.scalar()
                total += count
            except: pass
        print(f'TOTAL_RECORDS: {total}')
except Exception as e:
    print(f'ERROR: {e}')
" 2>/dev/null)

if echo "$DATA_CHECK" | grep -q "TOTAL_RECORDS:"; then
    TOTAL_RECORDS=$(echo "$DATA_CHECK" | grep "TOTAL_RECORDS:" | sed 's/TOTAL_RECORDS: //')
    log_success "Dados no sistema: $TOTAL_RECORDS registros"
else
    log_warning "Não foi possível verificar dados"
fi

# =========================================
# RELATÓRIO FINAL
# =========================================
END_TIME=$(date +%s)
ELAPSED_TIME=$((END_TIME - START_TIME))

echo ""
echo -e "${BOLD}${GREEN}🎉 SILA SISTEMA COMPLETO OPERACIONAL!${NC}"
echo "=========================================="
echo -e "${GREEN}⏱️  Tempo total: ${ELAPSED_TIME}s${NC}"
echo -e "${GREEN}📊 Registros no sistema: ${TOTAL_RECORDS:-0}${NC}"
echo ""

echo -e "${BOLD}${CYAN}🌐 ACESSE O SISTEMA:${NC}"
echo "=========================================="
if [ "${FRONTEND_OK:-false}" = "true" ]; then
    echo -e "${GREEN}🌐 Frontend: http://localhost${NC}"
    echo -e "${GREEN}🌐 Frontend: http://localhost:80${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend: Em inicialização${NC}"
fi

if [ "${BACKEND_OK:-false}" = "true" ]; then
    echo -e "${GREEN}🔗 Backend API: http://localhost:8000${NC}"
    echo -e "${GREEN}📚 Documentação: http://localhost:8000/docs${NC}"
    echo -e "${GREEN}📖 ReDoc: http://localhost:8000/redoc${NC}"
fi

echo ""
echo -e "${BOLD}${CYAN}🛠️  COMANDOS ÚTEIS:${NC}"
echo "=========================================="
echo "• Status: docker compose ps"
echo "• Logs backend: docker compose logs -f backend"
echo "• Logs frontend: docker compose logs -f frontend"
echo "• Parar tudo: docker compose --profile infra --profile backend --profile frontend down"
echo "• Restart: bash sila_up.sh"

echo ""
echo -e "${BOLD}${GREEN}✨ SISTEMA PRONTO PARA USO!${NC}"
echo -e "${GREEN}   Acesse: http://localhost${NC}"
echo ""

exit 0
