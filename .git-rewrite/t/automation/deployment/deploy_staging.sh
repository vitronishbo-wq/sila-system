#!/bin/bash
# Script de Deploy para Staging do SILA System
# Executa deploy completo com validação, healthcheck e rollback automático
# Uso: ./scripts/deploy_staging.sh

set -euo pipefail

# --- Patch Anti-Panic do Docker Compose ---
export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export COMPOSE_DOCKER_CLI_BUILD=1

# --- Configurações ---
ENVIRONMENT="staging"
HEALTHCHECK_URL="http://localhost:9111/health"
METRICS_URL="http://localhost:9111/metrics"
MAX_WAIT_SECONDS=120
WAIT_INTERVAL=10
BACKUP_DIR="/opt/sila-backups"

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
        FATAL)
            echo -e "[${timestamp}] ${RED}[FATAL]${NC} $message"
            ;;
        *)
            echo -e "[${timestamp}] [${level}] $message"
            ;;
    esac
}

# Banner
echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║           🚀 SILA System - Staging Deployment                ║
║              Validação, Deploy e Monitoramento               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# --- Funções de Validação ---

validate_environment() {
    log INFO "Validando ambiente staging..."

    # Verificar se estamos no diretório correto
    if [[ ! -f "docker-compose.yml" ]]; then
        log FATAL "docker-compose.yml não encontrado. Execute do diretório raiz do projeto."
        exit 1
    fi

    # Verificar arquivo .env.staging
    if [[ ! -f ".env.staging" ]]; then
        log FATAL ".env.staging não encontrado!"
        exit 1
    fi

    # Verificar variáveis críticas
    source .env.staging

    local required_vars=(
        "DATABASE_URL"
        "SECRET_KEY"
        "JWT_SECRET_KEY"
    )

    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            log FATAL "Variável obrigatória não definida: $var"
            exit 1
        fi

        # Verificar se não está usando valores padrão inseguros
        if [[ "${!var}" == *"CHANGE_ME"* ]]; then
            log FATAL "Variável $var ainda contém valor padrão CHANGE_ME"
            exit 1
        fi
    done

    log SUCCESS "Ambiente validado"
}

validate_dependencies() {
    log INFO "Validando dependências..."

    local missing_deps=()

    if ! command -v docker &> /dev/null; then
        missing_deps+=("docker")
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        missing_deps+=("docker-compose")
    fi

    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi

    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log FATAL "Dependências faltando: ${missing_deps[*]}"
        exit 1
    fi

    log SUCCESS "Dependências validadas"
}

# --- Funções de Backup ---

backup_database() {
    log INFO "Criando backup do banco de dados..."

    # Criar diretório de backup se não existir
    mkdir -p "$BACKUP_DIR"

    local backup_file="${BACKUP_DIR}/sila_staging_$(date +%Y%m%d_%H%M%S).sql"

    # Determinar comando docker compose
    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Executar backup
    if $compose_cmd exec -T postgres pg_dump -U sila_staging sila_staging > "$backup_file" 2>/dev/null; then
        log SUCCESS "Backup criado: $backup_file"

        # Comprimir backup
        gzip "$backup_file"
        log SUCCESS "Backup comprimido: ${backup_file}.gz"

        # Limpar backups antigos (manter últimos 7 dias)
        find "$BACKUP_DIR" -name "sila_staging_*.sql.gz" -mtime +7 -delete
        log INFO "Backups antigos removidos"
    else
        log WARN "Não foi possível criar backup (banco pode não estar rodando)"
    fi
}

backup_containers() {
    log INFO "Salvando estado atual dos containers..."

    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Salvar lista de containers ativos
    $compose_cmd ps > "${BACKUP_DIR}/containers_state_$(date +%Y%m%d_%H%M%S).txt" || true

    log SUCCESS "Estado dos containers salvo"
}

# --- Funções de Deploy ---

pull_latest_code() {
    log INFO "Atualizando código do repositório..."

    # Verificar branch atual
    local current_branch=$(git branch --show-current)
    log INFO "Branch atual: $current_branch"

    # Pull das últimas mudanças
    git fetch origin
    git pull origin staging

    local commit_hash=$(git rev-parse --short HEAD)
    log SUCCESS "Código atualizado para commit: $commit_hash"
}

build_and_deploy() {
    log INFO "Iniciando build e deploy..."

    # Determinar comando docker compose
    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Exportar variáveis de ambiente
    export ENVIRONMENT=staging
    export NODE_ENV=staging

    # Criar link simbólico para .env
    ln -sf .env.staging .env

    # Derrubar containers antigos
    log INFO "Parando containers antigos..."
    $compose_cmd down -t 30 --remove-orphans

    # Build das imagens
    log INFO "Construindo imagens Docker..."
    $compose_cmd build --no-cache --pull

    # Subir novos containers
    log INFO "Iniciando novos containers..."
    $compose_cmd --profile backend --profile frontend up -d --wait

    log SUCCESS "Deploy concluído"
}

# --- Funções de Healthcheck ---

wait_for_service() {
    local url=$1
    local max_seconds=$2
    local interval=$3
    local elapsed=0

    log INFO "Aguardando serviço: $url"

    while [[ $elapsed -lt $max_seconds ]]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            log SUCCESS "Serviço em $url está UP!"
            return 0
        fi

        log INFO "Aguardando... (${elapsed}s/${max_seconds}s)"
        sleep "$interval"
        elapsed=$((elapsed + interval))
    done

    log ERROR "Timeout aguardando serviço: $url"
    return 1
}

run_healthchecks() {
    log INFO "Executando healthchecks..."

    # Healthcheck do backend
    if ! wait_for_service "$HEALTHCHECK_URL" "$MAX_WAIT_SECONDS" "$WAIT_INTERVAL"; then
        log FATAL "Backend healthcheck falhou!"
        return 1
    fi

    # Verificar métricas
    log INFO "Verificando endpoint de métricas..."
    if curl -s -f "$METRICS_URL" | head -n 5 > /dev/null 2>&1; then
        log SUCCESS "Métricas disponíveis"
    else
        log WARN "Métricas não disponíveis"
    fi

    # Verificar API docs
    log INFO "Verificando API docs..."
    if curl -s -f "http://localhost:8000/docs" > /dev/null 2>&1; then
        log SUCCESS "API docs disponível"
    else
        log WARN "API docs não disponível"
    fi

    log SUCCESS "Healthchecks concluídos"
}

run_smoke_tests() {
    log INFO "Executando smoke tests..."

    local endpoints=(
        "http://localhost:8000/health"
        "http://localhost:8000/docs"
        "http://localhost:9111/health"
        "http://localhost:9111/metrics"
    )

    local failed=0

    for endpoint in "${endpoints[@]}"; do
        if curl -s -f "$endpoint" > /dev/null 2>&1; then
            log SUCCESS "✅ $endpoint"
        else
            log ERROR "❌ $endpoint"
            failed=$((failed + 1))
        fi
    done

    if [[ $failed -gt 0 ]]; then
        log ERROR "$failed smoke tests falharam"
        return 1
    fi

    log SUCCESS "Todos os smoke tests passaram!"
    return 0
}

# --- Funções de Monitoramento ---

check_container_health() {
    log INFO "Verificando saúde dos containers..."

    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Listar containers
    echo ""
    echo -e "${CYAN}Status dos Containers:${NC}"
    $compose_cmd ps
    echo ""

    # Verificar containers unhealthy
    local unhealthy=$($compose_cmd ps --filter "health=unhealthy" -q | wc -l)

    if [[ $unhealthy -gt 0 ]]; then
        log WARN "$unhealthy containers não estão saudáveis"
        return 1
    fi

    log SUCCESS "Todos os containers estão saudáveis"
}

show_logs() {
    log INFO "Últimas linhas dos logs:"

    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    echo ""
    echo -e "${CYAN}=== Backend Logs ===${NC}"
    $compose_cmd logs --tail=20 backend

    echo ""
    echo -e "${CYAN}=== Frontend Logs ===${NC}"
    $compose_cmd logs --tail=20 frontend || log WARN "Frontend logs não disponíveis"
}

# --- Funções de Rollback ---

rollback() {
    log ERROR "Iniciando rollback..."

    local compose_cmd="docker-compose"
    if docker compose version &> /dev/null; then
        compose_cmd="docker compose"
    fi

    # Derrubar containers atuais
    $compose_cmd down -t 10

    # Restaurar backup do banco (se disponível)
    local latest_backup=$(ls -t ${BACKUP_DIR}/sila_staging_*.sql.gz 2>/dev/null | head -n 1)

    if [[ -n "$latest_backup" ]]; then
        log INFO "Restaurando backup: $latest_backup"
        gunzip -c "$latest_backup" | $compose_cmd exec -T postgres psql -U sila_staging sila_staging || true
    fi

    log ERROR "Rollback concluído. Verifique os logs e tente novamente."
    exit 1
}

# --- Função Principal ---

main() {
    local start_time=$(date +%s)

    log INFO "Iniciando deploy para staging..."

    # Validações
    validate_dependencies
    validate_environment

    # Backups
    backup_database
    backup_containers

    # Deploy
    pull_latest_code
    build_and_deploy

    # Healthchecks
    if ! run_healthchecks; then
        log FATAL "Healthchecks falharam!"
        rollback
    fi

    # Smoke tests
    if ! run_smoke_tests; then
        log FATAL "Smoke tests falharam!"
        rollback
    fi

    # Verificar saúde dos containers
    check_container_health || log WARN "Alguns containers podem não estar completamente saudáveis"

    # Mostrar logs
    show_logs

    # Calcular tempo de deploy
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    # Sucesso!
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║              ✅ Deploy Staging Concluído!                    ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    log SUCCESS "Deploy concluído em ${duration}s"

    echo ""
    echo -e "${CYAN}📊 Informações do Deploy:${NC}"
    echo -e "   Ambiente:     ${YELLOW}staging${NC}"
    echo -e "   Commit:       ${YELLOW}$(git rev-parse --short HEAD)${NC}"
    echo -e "   Duração:      ${YELLOW}${duration}s${NC}"
    echo -e "   Timestamp:    ${YELLOW}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo ""

    echo -e "${CYAN}🌐 URLs Disponíveis:${NC}"
    echo -e "   API:          ${GREEN}http://localhost:8000${NC}"
    echo -e "   Docs:         ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "   Healthcheck:  ${GREEN}http://localhost:9111/health${NC}"
    echo -e "   Métricas:     ${GREEN}http://localhost:9111/metrics${NC}"
    echo ""

    echo -e "${CYAN}🔧 Comandos Úteis:${NC}"
    echo -e "   Status:       ${YELLOW}./status_sila.sh${NC}"
    echo -e "   Logs:         ${YELLOW}docker compose logs -f${NC}"
    echo -e "   Parar:        ${YELLOW}./sila_stop.sh${NC}"
    echo ""
}

# --- Entry Point ---

# Trap para rollback em caso de erro
trap 'rollback' ERR

main "$@"
