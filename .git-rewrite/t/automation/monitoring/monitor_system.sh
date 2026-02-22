#!/bin/bash
# Script de Monitoramento Contínuo do SILA System
# Monitora saúde, performance e recursos dos containers
# Uso: ./scripts/monitor_system.sh [interval_seconds]

set -euo pipefail

# --- Patch Anti-Panic do Docker Compose ---
export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export COMPOSE_DOCKER_CLI_BUILD=1

# --- Configurações ---
INTERVAL="${1:-30}"  # Intervalo de monitoramento em segundos
HEALTHCHECK_URL="http://localhost:9111/health"
METRICS_URL="http://localhost:9111/metrics"
LOG_FILE="/var/log/sila/monitor.log"
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEMORY=80
ALERT_THRESHOLD_DISK=90

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# --- Funções de Logging ---

log() {
    local level=$1
    local message=$2
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')

    local log_entry="[${timestamp}] [${level}] $message"

    # Output colorido no terminal
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
        ALERT)
            echo -e "[${timestamp}] ${RED}[ALERT]${NC} $message"
            ;;
        *)
            echo -e "[${timestamp}] [${level}] $message"
            ;;
    esac

    # Salvar em arquivo de log (se possível)
    if [[ -w "$(dirname "$LOG_FILE")" ]] 2>/dev/null; then
        echo "$log_entry" >> "$LOG_FILE"
    fi
}

# Banner
clear
echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║          📊 SILA System - Continuous Monitoring              ║
║              Healthcheck, Metrics & Alerts                   ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# --- Funções de Monitoramento ---

check_healthcheck() {
    if curl -s -f "$HEALTHCHECK_URL" > /dev/null 2>&1; then
        log SUCCESS "Healthcheck: OK"
        return 0
    else
        log ERROR "Healthcheck: FAILED"
        return 1
    fi
}

get_container_stats() {
    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Obter estatísticas dos containers
    local stats=$($compose_cmd ps --format json 2>/dev/null || echo "[]")

    echo "$stats"
}

monitor_container_resources() {
    log INFO "Monitorando recursos dos containers..."

    # Obter estatísticas de CPU e memória
    local stats=$(docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "")

    if [[ -z "$stats" ]]; then
        log WARN "Não foi possível obter estatísticas dos containers"
        return 1
    fi

    echo ""
    echo -e "${CYAN}=== Container Resources ===${NC}"
    echo "$stats"
    echo ""

    # Verificar thresholds e alertar
    while IFS= read -r line; do
        if [[ "$line" =~ CONTAINER ]]; then
            continue
        fi

        local container=$(echo "$line" | awk '{print $1}')
        local cpu=$(echo "$line" | awk '{print $2}' | sed 's/%//')
        local mem=$(echo "$line" | awk '{print $3}' | sed 's/%//')

        # Alertar se CPU alta
        if [[ -n "$cpu" ]] && (( $(echo "$cpu > $ALERT_THRESHOLD_CPU" | bc -l 2>/dev/null || echo 0) )); then
            log ALERT "Container $container: CPU alta (${cpu}%)"
        fi

        # Alertar se memória alta
        if [[ -n "$mem" ]] && (( $(echo "$mem > $ALERT_THRESHOLD_MEMORY" | bc -l 2>/dev/null || echo 0) )); then
            log ALERT "Container $container: Memória alta (${mem}%)"
        fi
    done <<< "$stats"
}

monitor_disk_usage() {
    log INFO "Monitorando uso de disco..."

    local disk_usage=$(df -h / | tail -n 1 | awk '{print $5}' | sed 's/%//')

    echo -e "${CYAN}Uso de Disco:${NC} ${disk_usage}%"

    if [[ $disk_usage -gt $ALERT_THRESHOLD_DISK ]]; then
        log ALERT "Uso de disco crítico: ${disk_usage}%"
    fi
}

check_container_health_status() {
    log INFO "Verificando status de saúde dos containers..."

    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Listar containers
    local containers=$($compose_cmd ps --format "{{.Service}}" 2>/dev/null || echo "")

    if [[ -z "$containers" ]]; then
        log WARN "Nenhum container encontrado"
        return 1
    fi

    echo ""
    echo -e "${CYAN}=== Container Health Status ===${NC}"

    for service in $containers; do
        local status=$($compose_cmd ps "$service" --format "{{.Status}}" 2>/dev/null || echo "unknown")

        if [[ "$status" =~ "Up" ]] && [[ "$status" =~ "healthy" ]]; then
            echo -e "  ${GREEN}✅${NC} $service: $status"
        elif [[ "$status" =~ "Up" ]]; then
            echo -e "  ${YELLOW}⚠️${NC} $service: $status"
        else
            echo -e "  ${RED}❌${NC} $service: $status"
            log ERROR "Container $service não está rodando corretamente"
        fi
    done
    echo ""
}

fetch_metrics() {
    log INFO "Coletando métricas..."

    if ! curl -s -f "$METRICS_URL" > /dev/null 2>&1; then
        log WARN "Endpoint de métricas não disponível"
        return 1
    fi

    # Obter métricas principais
    local metrics=$(curl -s "$METRICS_URL" 2>/dev/null || echo "")

    if [[ -z "$metrics" ]]; then
        return 1
    fi

    echo ""
    echo -e "${CYAN}=== Application Metrics ===${NC}"

    # Extrair métricas relevantes (exemplo)
    echo "$metrics" | grep -E "^(http_requests_total|http_request_duration|process_cpu_seconds)" | head -n 10 || echo "Métricas não disponíveis"
    echo ""
}

check_logs_for_errors() {
    log INFO "Verificando logs por erros recentes..."

    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Verificar últimas 50 linhas dos logs do backend
    local error_count=$($compose_cmd logs --tail=50 backend 2>/dev/null | grep -i "error\|exception\|fatal" | wc -l || echo "0")

    if [[ $error_count -gt 0 ]]; then
        log WARN "Encontrados $error_count erros nos logs recentes do backend"

        echo ""
        echo -e "${YELLOW}Últimos erros:${NC}"
        $compose_cmd logs --tail=50 backend 2>/dev/null | grep -i "error\|exception\|fatal" | tail -n 5
        echo ""
    else
        log SUCCESS "Nenhum erro encontrado nos logs recentes"
    fi
}

check_database_connection() {
    log INFO "Verificando conexão com banco de dados..."

    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Tentar conectar ao PostgreSQL
    if $compose_cmd exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
        log SUCCESS "Banco de dados: OK"
        return 0
    else
        log ERROR "Banco de dados: FALHA na conexão"
        return 1
    fi
}

generate_summary() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                    Monitoring Summary                        ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  Timestamp:     $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "  Next check in: ${INTERVAL}s"
    echo ""
}

# --- Função Principal ---

monitor_loop() {
    log INFO "Iniciando monitoramento contínuo (intervalo: ${INTERVAL}s)"
    log INFO "Pressione Ctrl+C para parar"
    echo ""

    local iteration=0

    while true; do
        iteration=$((iteration + 1))

        echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${PURPLE}  Iteration #${iteration} - $(date '+%Y-%m-%d %H:%M:%S')${NC}"
        echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""

        # Executar verificações
        check_healthcheck || true
        check_database_connection || true
        check_container_health_status || true
        monitor_container_resources || true
        monitor_disk_usage || true
        fetch_metrics || true
        check_logs_for_errors || true

        # Resumo
        generate_summary

        # Aguardar próximo ciclo
        sleep "$INTERVAL"

        # Limpar tela a cada 10 iterações
        if (( iteration % 10 == 0 )); then
            clear
            echo -e "${PURPLE}"
            cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║          📊 SILA System - Continuous Monitoring              ║
╚═══════════════════════════════════════════════════════════════╝
EOF
            echo -e "${NC}"
        fi
    done
}

# --- Entry Point ---

# Trap para limpeza
trap 'echo ""; log INFO "Monitoramento interrompido pelo usuário"; exit 0' SIGINT SIGTERM

monitor_loop
