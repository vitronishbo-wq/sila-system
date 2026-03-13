#!/bin/bash
# =============================================================================
# SILA SYSTEM - Backend Startup Manager
# =============================================================================
# Script robusto para inicialização do ecossistema backend
# =============================================================================

set -euo pipefail

# Cores para feedback
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly RED='\033[0;31m'
readonly NC='\033[0m'

# Caminhos base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# 1. Verificação de Variáveis de Ambiente
log "Validando arquivos de configuração..."
if [ ! -f "apps/backend/.env" ]; then
    if [ -f "apps/backend/.env.example" ]; then
        warn "Arquivo .env não encontrado. Criando a partir do .env.example..."
        cp apps/backend/.env.example apps/backend/.env
    else
        error "Arquivo .env.example não encontrado em apps/backend/"
    fi
fi

# 2. Configuração de Perfil
APP_ENV=${APP_ENV:-development}
log "Iniciando em modo: $APP_ENV"

# 3. Limpeza de Segurança (Evita conflitos de rede ou volumes corrompidos)
if [ "${CLEAN_START:-false}" = "true" ]; then
    log "Limpando containers e redes antigas..."
    docker compose down --remove-orphans
fi

# 4. Verificação/Criação de Redes Externas
log "Configurando rede do sistema..."
docker network inspect sila-network >/dev/null 2>&1 || \
    docker network create sila-network

# 5. Build e Execução
# Se FORCE_REBUILD for true, força a recompilação das imagens
BUILD_FLAG=""
if [ "${FORCE_REBUILD:-false}" = "true" ]; then
    BUILD_FLAG="--build"
    log "Forçando rebuild das imagens..."
fi

log "Subindo os serviços (Banco, Redis, Backend, Workers)..."
if [ "$APP_ENV" = "production" ]; then
    docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d $BUILD_FLAG
else
    # Em desenvolvimento, usamos o override para volumes e reload automático
    docker compose -f docker-compose.yml -f docker-compose.override.yml up -d $BUILD_FLAG
fi

# 6. Verificação de Saúde
log "Aguardando inicialização dos serviços..."
sleep 5

if docker compose ps | grep -q "Exit"; then
    error "Um ou mais serviços falharam ao iniciar. Verifique 'docker compose logs'."
else
    log "======================================================"
    log "✅ SILA Backend iniciado com sucesso!"
    log "API: http://localhost:8000"
    log "Flower (Tasks): http://localhost:5555"
    log "Documentação: http://localhost:8000/docs"
    log "======================================================"
fi