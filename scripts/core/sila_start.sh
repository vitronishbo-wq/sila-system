#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

export POSTGRES_PASSWORD=Trumanmarcelo_1983
export DATABASE_URL="postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_db"

SERVICE_HEALTHCHECK_URL="http://localhost:8000/health"
SERVICE_METRICS_URL="http://localhost:8000/metrics"
MAX_WAIT_SECONDS=60
WAIT_INTERVAL=5

log_info() { log_level INFO "$1"; }
log_success() { log_level SUCCESS "$1"; }
log_warning() { log_level WARN "$1"; }
log_error() { log_level ERROR "$1"; }

detect_mode() {
    local arg="${1:-}"
    case "$arg" in
        dev|development) echo "development" ;;
        prod|production) echo "production" ;;
        *) [[ -f ".env.production" ]] && echo "production" || echo "development" ;;
    esac
}

check_dependencies() {
    log INFO "Verificando Docker e Curl..."
    command -v docker &> /dev/null || exit 1
    command -v curl &> /dev/null || exit 1
}

cleanup_on_interrupt() {
    log WARN "Interrupção detectada..."
    docker compose down -t 5 --remove-orphans 2>/dev/null || true
    exit 1
}

trap cleanup_on_interrupt SIGINT SIGTERM

setup_environment() {
    local mode=$1
    local env_file=".env.${mode}"
    if [[ ! -f "$env_file" ]]; then
        [[ -f ".env.template" ]] && cp ".env.template" "$env_file" || exit 1
        sed -i "s/ENVIRONMENT=.*/ENVIRONMENT=$mode/" "$env_file"
    fi
    set -a
    source "$env_file"
    set +a
    ln -sf "$env_file" ".env"
}

start_services() {
    log INFO "Subindo stack SILA System..."
    docker compose --profile backend --profile frontend up --build -d
}

wait_for_service() {
    local url=$1
    local elapsed=0
    while [[ $elapsed -lt $MAX_WAIT_SECONDS ]]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            return 0
        fi
        sleep "$WAIT_INTERVAL"
        elapsed=$((elapsed + WAIT_INTERVAL))
    done
    return 1
}

main() {
    local mode=$(detect_mode "${1:-}")
    check_dependencies
    setup_environment "$mode"
    
    if [[ "${2:-}" == "--clean" ]]; then
        docker compose down -v --remove-orphans 2>/dev/null || true
    fi

    start_services
    wait_for_service "$SERVICE_HEALTHCHECK_URL" || {
        log ERROR "Backend não iniciou."
        docker compose logs backend | tail -n 20
        exit 1
    }
    log SUCCESS "SILA System rodando em http://localhost:5173"
}

main "$@"