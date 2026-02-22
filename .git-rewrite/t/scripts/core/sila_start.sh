#!/bin/bash
# ===========================================
# SILA System - Script de Inicialização MSIC
# Metodologia SILA de Intercâmbio de Configurações
# Versão: 4.0 - Profissional com Logging Estruturado
# ===========================================

set -euo pipefail

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

# --- Patch Anti-Panic do Docker Compose ---
# Desabilita hints, telemetria e avisos desnecessários
export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0

# --- Configurações ---
SERVICE_HEALTHCHECK_URL="http://localhost:8000/health"
SERVICE_METRICS_URL="http://localhost:8000/metrics"
MAX_WAIT_SECONDS=60
WAIT_INTERVAL=5
FRONTEND_DIR="frontend"

# Banner MSIC
echo -e "${MAGENTA}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                    🚀 SILA SYSTEM 4.0 MSIC                   ║
║         Metodologia SILA de Intercâmbio de Configurações     ║
║         Docker Compose Unificado com Healthcheck Ativo       ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Aliases para compatibilidade com código existente
log_info() {
    log_level INFO "$1"
}

log_success() {
    log_level SUCCESS "$1"
}

log_warning() {
    log_level WARN "$1"
}

log_error() {
    log_level ERROR "$1"
}

# Detectar modo de execução
detect_mode() {
    local arg="${1:-}"

    case "$arg" in
        dev|development)
            echo "development"
            ;;
        prod|production)
            echo "production"
            ;;
        staging)
            echo "staging"
            ;;
        *)
            # Auto-detectar baseado nos arquivos .env disponíveis
            if [[ -f ".env.development" ]]; then
                echo "development"
            elif [[ -f ".env.production" ]]; then
                echo "production"
            else
                echo "development"  # Default
            fi
            ;;
    esac
}

# Verificar dependências do sistema
check_dependencies() {
    log INFO "Verificando dependências essenciais (Docker e Curl)..."

    local missing_deps=()

    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        missing_deps+=("docker")
    fi

    # Verificar Docker Compose
    if ! docker compose version &> /dev/null; then
        missing_deps+=("docker-compose")
    fi

    # Verificar Curl
    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log ERROR "Dependências faltando: ${missing_deps[*]}"
        log INFO "Instale as dependências e tente novamente."
        exit 1
    fi

    log SUCCESS "Todas as dependências verificadas"
}

# Função de limpeza em caso de interrupção
cleanup_on_interrupt() {
    log WARN "Interrupção detectada (Ctrl+C). Tentando derrubar os containers..."
    if [[ -f "./sila_stop.sh" ]]; then
        ./sila_stop.sh || true
    else
        docker compose down -t 10 --remove-orphans 2>/dev/null || docker-compose down -t 10 --remove-orphans 2>/dev/null || true
    fi
    exit 1
}

# Configurar trap para limpeza em caso de interrupção
trap cleanup_on_interrupt SIGINT SIGTERM

# Verificar arquivos essenciais
check_essential_files() {
    log_info "Verificando arquivos essenciais..."

    local missing_files=()

    [[ ! -f "docker-compose.yml" ]] && missing_files+=("docker-compose.yml")
    [[ ! -f "backend/Dockerfile" ]] && missing_files+=("backend/Dockerfile")
    [[ ! -f "backend/config/settings.py" ]] && missing_files+=("backend/config/settings.py")

    if [[ ${#missing_files[@]} -gt 0 ]]; then
        log_error "Arquivos essenciais faltando:"
        printf '  - %s\n' "${missing_files[@]}"
        exit 1
    fi

    log_success "Todos os arquivos essenciais encontrados"
}

# Configurar ambiente
setup_environment() {
    local mode=$1

    log INFO "Ambiente selecionado: ${mode}"

    # Verificar se existe arquivo .env para o modo
    local env_file=".env.${mode}"

    if [[ ! -f "$env_file" ]]; then
        log WARN "Arquivo $env_file não encontrado"

        # Verificar se existe .env.template
        if [[ -f ".env.template" ]]; then
            log INFO "Gerando $env_file a partir de .env.template..."
            cp ".env.template" "$env_file"

            # Ajustar variáveis específicas do ambiente
            sed -i "s/ENVIRONMENT=.*/ENVIRONMENT=$mode/" "$env_file"
            sed -i "s/NODE_ENV=.*/NODE_ENV=$mode/" "$env_file"

            if [[ "$mode" == "development" ]]; then
                sed -i "s/DEBUG=.*/DEBUG=True/" "$env_file"
                sed -i "s/LOG_LEVEL=.*/LOG_LEVEL=INFO/" "$env_file"
                sed -i "s/FRONTEND_TARGET=.*/FRONTEND_TARGET=dev/" "$env_file"
            else
                sed -i "s/DEBUG=.*/DEBUG=False/" "$env_file"
                sed -i "s/LOG_LEVEL=.*/LOG_LEVEL=WARNING/" "$env_file"
                sed -i "s/FRONTEND_TARGET=.*/FRONTEND_TARGET=runtime/" "$env_file"
            fi

            log SUCCESS "Arquivo $env_file criado"
        else
            log ERROR "Arquivo .env.template não encontrado!"
            log INFO "Execute: cp .env.example .env.template"
            exit 1
        fi
    fi

    log INFO "Carregando variáveis de ambiente de $env_file..."
    # Exportar todas as variáveis do arquivo
    set -a
    if [[ -f "$env_file" ]]; then
        source "$env_file"
    fi
    set +a

    # Exportar variáveis adicionais
    export ENVIRONMENT=$mode
    export NODE_ENV=$mode
    export FRONTEND_TARGET=$([ "$mode" = "development" ] && echo "dev" || echo "runtime")
    export DEBUG=$([ "$mode" = "development" ] && echo "true" || echo "false")

    # Criar link simbólico .env -> .env.{mode}
    ln -sf "$env_file" ".env"

    log SUCCESS "Ambiente configurado para $mode"
}

# Limpar containers e volumes antigos
cleanup_old_containers() {
    log_info "Limpando containers antigos..."

    # Parar containers do SILA
    docker compose down --remove-orphans 2>/dev/null || docker-compose down --remove-orphans 2>/dev/null || true

    # Remover containers órfãos
    docker container prune -f 2>/dev/null || true

    log_success "Limpeza concluída"
}

# Preparar e construir frontend
prepare_frontend() {
    local mode=$1

    if [[ "$mode" == "development" ]] || [[ "$mode" == "dev" ]]; then
        log INFO "Modo DEV. Iniciando build do frontend (usando o script auxiliar)..."
        if [[ -f "automation/maintenance/build_frontend.sh" ]]; then
            bash automation/maintenance/build_frontend.sh dev
        else
            log WARN "Script automation/maintenance/build_frontend.sh não encontrado. Pulando build do frontend."
        fi
    fi
}

# Iniciar serviços
start_services() {
    local mode=$1

    log INFO "Subindo stack SILA System (perfis backend e frontend)..."

    # Determinar comando docker compose
    local compose_cmd="docker compose"
    if ! docker compose version &> /dev/null; then
        compose_cmd="docker-compose"
    fi

    # Construir e iniciar serviços com --wait para espera inteligente
    if [[ "$mode" == "development" ]]; then
        log INFO "🔥 Modo desenvolvimento - Hot reload ativado"
        $compose_cmd --profile backend --profile frontend up --build -d
    else
        log INFO "🏭 Modo produção - Executando em background"
        $compose_cmd --profile backend --profile frontend up --build -d
    fi
}

# Função de espera inteligente para serviços
wait_for_service() {
    local url=$1
    local max_seconds=$2
    local interval=$3
    local elapsed=0

    while [[ $elapsed -lt $max_seconds ]]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            log SUCCESS "Serviço em $url está UP e OK."
            return 0
        fi
        log INFO "Aguardando o serviço... (Tentativa em ${elapsed}/${max_seconds}s)"
        sleep "$interval"
        elapsed=$((elapsed + interval))
    done

    log ERROR "O serviço em $url não respondeu ao healthcheck após ${max_seconds} segundos."
    return 1
}

# Verificar saúde dos serviços com healthcheck HTTP
check_services_health() {
    log INFO "Iniciando rotina de Healthcheck em ${SERVICE_HEALTHCHECK_URL} (Máximo ${MAX_WAIT_SECONDS}s)..."

    wait_for_service "$SERVICE_HEALTHCHECK_URL" "$MAX_WAIT_SECONDS" "$WAIT_INTERVAL"

    if [[ $? -ne 0 ]]; then
        log FATAL "Falha crítica: O backend não iniciou corretamente. Verifique os logs."
        docker compose logs backend 2>/dev/null || docker-compose logs backend 2>/dev/null || true

        # Tentar derrubar os containers
        if [[ -f "./sila_stop.sh" ]]; then
            ./sila_stop.sh
        else
            docker compose down -t 10 --remove-orphans 2>/dev/null || true
        fi
        exit 1
    fi

    # Validar métricas
    log INFO "Validando a disponibilidade das métricas..."
    if curl -s "$SERVICE_METRICS_URL" | head -n 5 > /dev/null 2>&1; then
        log SUCCESS "Métricas disponíveis em ${SERVICE_METRICS_URL}"
    else
        log WARN "Métricas indisponíveis. Verifique o endpoint."
    fi
}

# Mostrar informações do sistema
show_system_info() {
    local mode=$1

    log SUCCESS "SILA System iniciado e saudável."
    echo ""
    echo "================================================="
    echo "        SILA System - URLs de Acesso"
    echo "================================================="
    echo "🔗 Ambiente:      ${mode}"
    echo "🔗 Frontend:      http://localhost:5173"
    echo "🔗 Backend (Docs):http://localhost:8000/docs"
    echo "🔗 Healthcheck:   ${SERVICE_HEALTHCHECK_URL}"
    echo "🔗 Métricas:      ${SERVICE_METRICS_URL}"
    echo "🔗 PostgreSQL:    localhost:5434"
    echo "================================================="
    echo ""

    echo -e "${CYAN}🔧 Comandos Úteis:${NC}"
    echo -e "   Parar:        ${YELLOW}./sila_stop.sh${NC}"
    echo -e "   Status:       ${YELLOW}./status_sila.sh${NC}"
    echo -e "   Logs:         ${YELLOW}docker compose logs -f${NC}"
    echo -e "   Logs Backend: ${YELLOW}docker compose logs -f backend${NC}"
    echo -e "   Logs Frontend:${YELLOW}docker compose logs -f frontend${NC}"
    echo -e "   Rebuild:      ${YELLOW}./sila_start.sh $mode${NC}"
    echo ""

    if [[ "$mode" == "production" ]]; then
        log WARN "Sistema rodando em background. Use 'docker compose logs -f' para ver logs."
    fi
}

# Função de ajuda
show_help() {
    cat << EOF
${CYAN}SILA System - Script de Inicialização MSIC${NC}

${YELLOW}Uso:${NC}
  $0 [modo] [opções]

${YELLOW}Modos:${NC}
  dev, development  - Modo desenvolvimento (hot reload, debug ativado)
  prod, production  - Modo produção (otimizado, background)
  staging           - Modo staging (testes pré-produção)
  (vazio)          - Auto-detectar baseado nos arquivos .env

${YELLOW}Opções:${NC}
  --help, -h       - Mostrar esta ajuda
  --clean          - Limpar volumes e reconstruir do zero

${YELLOW}Exemplos:${NC}
  $0                    # Auto-detectar modo
  $0 dev                # Modo desenvolvimento
  $0 prod               # Modo produção
  $0 dev --clean        # Desenvolvimento com limpeza completa

${YELLOW}Arquivos de Configuração (MSIC):${NC}
  .env.template         - Template base (não commitar com credenciais)
  .env.development      - Configuração de desenvolvimento
  .env.production       - Configuração de produção
  docker-compose.yml    - Orquestração unificada
  backend/config/settings.py - Configurações centralizadas (Pydantic V2)

EOF
}

# Garantir permissões de execução para scripts
ensure_script_permissions() {
    log INFO "Garantindo permissões de execução para automation/**/*.sh..."
    if [[ -d "automation" ]]; then
        find automation/ -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || log WARN "Não foi possível aplicar permissões. Ignorando."
    fi
}

# =========================
# FUNÇÃO PRINCIPAL
# =========================

main() {
    local mode=$(detect_mode "${1:-}")
    local clean_flag="${2:-}"

    echo -e "${BLUE}🎯 Modo detectado: $mode${NC}"
    echo ""

    # Executar verificações
    check_dependencies
    check_essential_files

    # Configurar ambiente
    setup_environment "$mode"

    # Garantir permissões de scripts
    ensure_script_permissions

    # Limpar se solicitado
    if [[ "$clean_flag" == "--clean" ]]; then
        log WARN "Limpeza completa solicitada..."
        docker compose down -v --remove-orphans 2>/dev/null || docker-compose down -v --remove-orphans 2>/dev/null || true
    else
        cleanup_old_containers
    fi

    # Preparar frontend (apenas em dev)
    prepare_frontend "$mode"

    # Iniciar serviços
    start_services "$mode"

    # Verificar saúde dos serviços
    check_services_health

    # Mostrar informações
    show_system_info "$mode"
}

# =========================
# ENTRY POINT
# =========================

case "${1:-}" in
    --help|-h)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
