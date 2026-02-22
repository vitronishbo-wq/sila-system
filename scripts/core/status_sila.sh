#!/bin/bash
# Script para verificar o status e healthcheck do SILA System
# Uso: ./status_sila.sh

set -euo pipefail

# --- Patch Anti-Panic do Docker Compose ---
export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export COMPOSE_DOCKER_CLI_BUILD=1

# --- Configurações ---
SERVICE_HEALTHCHECK_URL="http://localhost:8000/health"
SERVICE_METRICS_URL="http://localhost:8000/metrics"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║              🔍 SILA System - Status & Healthcheck           ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# 1. Listar o status dos containers
log INFO "Verificando o status atual dos containers via 'docker compose ps'..."
echo "-------------------------------------------------"
$COMPOSE_CMD ps
echo "-------------------------------------------------"
echo ""

# 2. Executar Healthcheck do Backend
log INFO "Executando Healthcheck no backend: ${SERVICE_HEALTHCHECK_URL}"

# Verificar se curl está disponível
if ! command -v curl &> /dev/null; then
    log ERROR "Curl não está instalado. Não é possível executar healthcheck HTTP."
else
    # Usamos -s (silencioso), -f (falhar em códigos HTTP > 400), e -o /dev/null (descartar saída)
    if curl -s -f -o /dev/null "$SERVICE_HEALTHCHECK_URL" 2>/dev/null; then
        log SUCCESS "BACKEND HEALTHCHECK: Status 200/OK (Serviço principal online)."
    else
        HEALTHCHECK_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_HEALTHCHECK_URL" 2>/dev/null || echo "ERRO")
        if [[ "$HEALTHCHECK_STATUS" = "000" ]] || [[ "$HEALTHCHECK_STATUS" = "ERRO" ]]; then
            log ERROR "BACKEND HEALTHCHECK: Falha na conexão (Serviço não responde na porta 8000)."
        else
            log ERROR "BACKEND HEALTHCHECK: Falha no Status ($HEALTHCHECK_STATUS). Verifique logs do backend."
        fi
    fi

    # Verificar métricas
    echo ""
    log INFO "Verificando disponibilidade das métricas..."
    if curl -s -f "$SERVICE_METRICS_URL" | head -n 3 > /dev/null 2>&1; then
        log SUCCESS "MÉTRICAS: Disponíveis em ${SERVICE_METRICS_URL}"
    else
        log WARN "MÉTRICAS: Indisponíveis ou inacessíveis."
    fi
fi

# 3. Status de Portas (apenas informativo)
echo ""
log INFO "Verificando portas de acesso..."

# Verificar se nc (netcat) está disponível
if command -v nc &> /dev/null; then
    if nc -z localhost 5173 2>/dev/null; then
        log SUCCESS "Porta 5173 (Frontend) está aberta."
    else
        log WARN "Porta 5173 (Frontend) está fechada."
    fi

    if nc -z localhost 8000 2>/dev/null; then
        log SUCCESS "Porta 8000 (Backend API) está aberta."
    else
        log WARN "Porta 8000 (Backend API) está fechada."
    fi

    # Porta 9111 removida - métricas agora estão na porta 8000

    if nc -z localhost 5434 2>/dev/null; then
        log SUCCESS "Porta 5434 (PostgreSQL) está aberta."
    else
        log WARN "Porta 5434 (PostgreSQL) está fechada."
    fi
else
    log WARN "Netcat (nc) não está instalado. Pulando verificação de portas."
fi

echo ""
log INFO "Verificação de status concluída."
echo ""
echo -e "${CYAN}💡 Dica: Use 'docker compose logs -f [service]' para ver logs em tempo real.${NC}"
