#!/bin/bash
# Script de Encerramento (Down) do SILA System
# Uso: ./sila_stop.sh

set -euo pipefail

# --- Patch Anti-Panic do Docker Compose ---
export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export COMPOSE_DOCKER_CLI_BUILD=1

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# --- Funções de Logging ---

log() {
    local level=$1
    local message=$2
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')

    case "$level" in
        INFO)
            echo -e "[${timestamp}] ${BLUE}[INFO]${NC} $message"
            ;;
        SUCCESS)
            echo -e "[${timestamp}] ${GREEN}[SUCCESS]${NC} $message"
            ;;
        WARN)
            echo -e "[${timestamp}] ${YELLOW}[WARN]${NC} $message"
            ;;
        ERROR)
            echo -e "[${timestamp}] ${RED}[ERROR]${NC} $message"
            ;;
        *)
            echo -e "[${timestamp}] [${level}] $message"
            ;;
    esac
}

# Determinar comando docker compose
COMPOSE_CMD="docker-compose"
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
fi

# 1. Checar se há containers ativos
log INFO "Verificando containers ativos do SILA System..."

if ! $COMPOSE_CMD ps --services 2>/dev/null | grep -q .; then
    log INFO "Nenhum container do SILA System ativo (docker compose ps vazio)."
    exit 0
fi

# 2. Derrubar a stack completa
log INFO "Iniciando o encerramento seguro (docker compose down)..."

# Usamos --remove-orphans e timeout de 10 segundos
# Removemos o -v por padrão para persistir dados (use --volumes se quiser limpar volumes)
$COMPOSE_CMD down -t 10 --remove-orphans

if [[ $? -eq 0 ]]; then
    log SUCCESS "SILA System encerrado com sucesso."
else
    log ERROR "Ocorreu um erro ao derrubar o Docker Compose. Verifique o status."
    exit 1
fi
