#!/bin/bash

# =================================================================
# SILA SYSTEM MONITOR - PAINEL TUI AVANÇADO
# Monitoramento interativo em tempo real com interface moderna
# Suporte a whiptail/dialog e fallback para interface de texto
# =================================================================

# ============================================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================================

# Detecta raiz do repositório quando executado dentro do código-fonte
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if git -C "$SCRIPT_DIR" rev-parse --show-toplevel >/dev/null 2>&1; then
    PROJECT_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
else
    PROJECT_ROOT="$SCRIPT_DIR"
fi

# Ambiente padrão de runtime (instalação) com fallback para o repo local
ENV_DIR="/opt/sila-system"
if [[ -d "$PROJECT_ROOT/infrastructure" ]] && [[ -f "$PROJECT_ROOT/infrastructure/docker/docker-compose.yml" ]]; then
    ENV_DIR="$PROJECT_ROOT"
fi

LOG_DIR="$ENV_DIR/logs"
BACKUP_DIR="$ENV_DIR/backups"
MONITOR_INTERVAL=5  # Segundos entre refresh automático
AUTO_REFRESH=false

# Diretório de relatórios estruturados de monitorização (quando em modo repo)
REPORT_DIR="$PROJECT_ROOT/reports/monitoring"

# Detectar se estamos em modo interativo
if [[ -n "${DISPLAY:-}" ]] && command -v whiptail >/dev/null 2>&1; then
    USE_WHIPTAIL=true
elif command -v dialog >/dev/null 2>&1; then
    USE_DIALOG=true
else
    USE_WHIPTAIL=false
    USE_DIALOG=false
fi

# ============================================================================
# CORES E FORMATAÇÃO AVANÇADA
# ============================================================================

# Cores modernas
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Ícones Unicode
CHECK_MARK="✅"
CROSS_MARK="❌"
WARNING="⚠️"
ROCKET="🚀"
PACKAGE="📦"
DOCKER="🐳"
GEAR="⚙️"
INFO="ℹ️"
SUCCESS="🎉"
MONITOR="📊"
CPU="🖥️"
MEMORY="🧠"
DISK="💽"
BACKUP="💾"
LOG="📄"

# ============================================================================
# DETECÇÃO DE AMBIENTE
# ============================================================================

detect_environment() {
    if [[ -f "$ENV_DIR/VERSION.txt" ]]; then
        CURRENT_VERSION=$(cat "$ENV_DIR/VERSION.txt" 2>/dev/null || echo "desconhecida")
    else
        CURRENT_VERSION="desconhecida"
    fi

    if [[ -f "$ENV_DIR/docker-compose.yml" ]] || [[ -f "$ENV_DIR/docker-compose.yaml" ]] || [[ -f "$PROJECT_ROOT/infrastructure/docker/docker-compose.yml" ]]; then
        DOCKER_ACTIVE=true
    else
        DOCKER_ACTIVE=false
    fi
}

# ============================================================================
# FUNÇÕES DE INTERFACE WHIPTAIL/DIALOG
# ============================================================================

show_main_menu_whiptail() {
    local choice
    choice=$(whiptail --title "SILA SYSTEM MONITOR" --menu "Escolha uma opção:" 20 60 8 \
        "1" "Containers Docker ativos" \
        "2" "Logs por ambiente" \
        "3" "Uso de CPU/RAM/Disco" \
        "4" "Últimos backups" \
        "5" "Status do sistema" \
        "6" "Configurações" \
        "7" "Sair" \
        3>&1 1>&2 2>&3)

    echo "$choice"
}

show_containers_whiptail() {
    local containers
    containers=$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}" 2>/dev/null || echo "Nenhum container ativo")

    whiptail --title "Containers Docker Ativos" --msgbox "$containers" 20 80
}

show_logs_whiptail() {
    local log_files
    log_files=$(ls -1t "$LOG_DIR"/deploy_*.log 2>/dev/null | head -5 | sed 's|.*/||' | nl -s ". ")

    if [[ -z "$log_files" ]]; then
        whiptail --title "Logs por Ambiente" --msgbox "Nenhum log encontrado em $LOG_DIR" 10 60
        return
    fi

    local choice
    choice=$(whiptail --title "Logs por Ambiente" --menu "Selecione um log para visualizar:" 15 60 5 \
        $(echo "$log_files" | sed 's/$/ ""/') \
        3>&1 1>&2 2>&3)

    if [[ -n "$choice" ]]; then
        local log_file="$LOG_DIR/$(echo "$log_files" | sed -n "${choice}p" | cut -d' ' -f2- | sed 's/^[0-9]*. //')"
        local log_content
        log_content=$(tail -n 20 "$log_file" 2>/dev/null || echo "Erro ao ler log")

        whiptail --title "Conteúdo do Log: $(basename "$log_file")" --msgbox "$log_content" 25 100
    fi
}

show_system_usage_whiptail() {
    local cpu_info
    cpu_info=$(top -bn1 | head -5 | tail -3)

    local mem_info
    mem_info=$(free -h)

    local disk_info
    disk_info=$(df -h | grep -E '^/dev' | head -3)

    local usage_info="$CPU $cpu_info\n\n$MEMORY\n$mem_info\n\n$DISK\n$disk_info"

    whiptail --title "Uso de Sistema" --msgbox "$usage_info" 20 80
}

show_backups_whiptail() {
    local backups
    backups=$(ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -5 | awk '{print $5 " " $9}' || echo "Nenhum backup encontrado")

    whiptail --title "Últimos Backups" --msgbox "$backups" 15 60
}

# ============================================================================
# FUNÇÕES DE INTERFACE DE TEXTO (FALLBACK)
# ============================================================================

show_main_menu_text() {
    clear
    echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}${BOLD}║                🖥️  SILA SYSTEM MONITOR TUI               ║${NC}"
    echo -e "${CYAN}${BOLD}╠══════════════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}${BOLD}║  ${GREEN}1${NC}. Containers Docker ativos                           ║${NC}"
    echo -e "${CYAN}${BOLD}║  ${BLUE}2${NC}. Logs por ambiente                                  ║${NC}"
    echo -e "${CYAN}${BOLD}║  ${YELLOW}3${NC}. Uso de CPU/RAM/Disco                              ║${NC}"
    echo -e "${CYAN}${BOLD}║  ${MAGENTA}4${NC}. Últimos backups                                   ║${NC}"
    echo -e "${CYAN}${BOLD}║  ${WHITE}5${NC}. Status do sistema                                 ║${NC}"
    echo -e "${CYAN}${BOLD}║  ${RED}6${NC}. Configurações                                     ║${NC}"
    echo -e "${CYAN}${BOLD}║  ${DIM}7${NC}. Sair                                              ║${NC}"
    echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}${INFO} Versão: ${NC}$CURRENT_VERSION"
    echo -e "${BLUE}${INFO} Ambiente: ${NC}$ENV_DIR"
    if [ "$AUTO_REFRESH" = true ]; then
        echo -e "${GREEN}${INFO} Refresh automático: ${MONITOR_INTERVAL}s${NC}"
    fi
    echo ""
    echo -n "Escolha uma opção [1-7]: "
}

show_containers_text() {
    echo -e "\n${DOCKER} ${BOLD}Containers Docker Ativos:${NC}\n"
    if command -v docker >/dev/null 2>&1; then
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}" || echo -e "${YELLOW}Docker não disponível ou nenhum container ativo${NC}"
    else
        echo -e "${RED}Docker não instalado${NC}"
    fi
    pause
}

show_logs_text() {
    echo -e "\n${LOG} ${BOLD}Logs por Ambiente:${NC}\n"

    if [[ ! -d "$LOG_DIR" ]]; then
        echo -e "${RED}Diretório de logs não encontrado: $LOG_DIR${NC}"
        pause
        return
    fi

    local log_files
    log_files=$(ls -1t "$LOG_DIR"/deploy_*.log 2>/dev/null | head -5)

    if [[ -z "$log_files" ]]; then
        echo -e "${YELLOW}Nenhum log de deploy encontrado${NC}"
        pause
        return
    fi

    echo -e "${BLUE}Arquivos de log disponíveis:${NC}"
    local count=1
    echo "$log_files" | while read -r log_file; do
        local base_name
        base_name=$(basename "$log_file")
        echo -e "  ${count}. $base_name"
        ((count++))
    done

    echo ""
    echo -n "Digite o número do log para visualizar (ou Enter para voltar): "
    read -r choice

    if [[ -n "$choice" ]] && [[ "$choice" =~ ^[0-9]+$ ]] && [[ $choice -ge 1 ]] && [[ $choice -le 5 ]]; then
        local selected_log
        selected_log=$(echo "$log_files" | sed -n "${choice}p")
        if [[ -f "$selected_log" ]]; then
            echo -e "\n${BOLD}Conteúdo do log: $(basename "$selected_log")${NC}"
            echo -e "${DIM}$(printf '═%.0s' $(tput cols))${NC}"
            tail -n 20 "$selected_log"
            echo -e "${DIM}$(printf '═%.0s' $(tput cols))${NC}"
        fi
    fi
    pause
}

show_system_usage_text() {
    echo -e "\n${MONITOR} ${BOLD}Uso de Sistema:${NC}\n"

    echo -e "${CPU} ${BOLD}CPU:${NC}"
    if command -v top >/dev/null 2>&1; then
        top -bn1 | head -3 | tail -2
    else
        echo -e "${YELLOW}Comando 'top' não disponível${NC}"
    fi

    echo -e "\n${MEMORY} ${BOLD}Memória:${NC}"
    if command -v free >/dev/null 2>&1; then
        free -h
    else
        echo -e "${YELLOW}Comando 'free' não disponível${NC}"
    fi

    echo -e "\n${DISK} ${BOLD}Disco:${NC}"
    if command -v df >/dev/null 2>&1; then
        df -h | grep -E '^/dev' | head -3
    else
        echo -e "${YELLOW}Comando 'df' não disponível${NC}"
    fi

    pause
}

show_backups_text() {
    echo -e "\n${BACKUP} ${BOLD}Últimos Backups:${NC}\n"

    if [[ ! -d "$BACKUP_DIR" ]]; then
        echo -e "${RED}Diretório de backups não encontrado: $BACKUP_DIR${NC}"
        pause
        return
    fi

    local backups
    backups=$(ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -5 | awk '{print "📦 " $5 " - " $9 " (" $1 ")" }' || echo "Nenhum backup encontrado")

    if [[ -z "$backups" ]] || [[ "$backups" == "Nenhum backup encontrado" ]]; then
        echo -e "${YELLOW}Nenhum backup encontrado em $BACKUP_DIR${NC}"
    else
        echo "$backups"
    fi
    pause
}

show_system_status_text() {
    echo -e "\n${GEAR} ${BOLD}Status do Sistema SILA:${NC}\n"

    echo -e "📍 Diretório: $ENV_DIR"
    echo -e "📦 Versão: $CURRENT_VERSION"
    echo -e "🐳 Docker: $(command -v docker >/dev/null 2>&1 && echo "${GREEN}Disponível${NC}" || echo "${RED}Não disponível${NC}")"
    echo -e "📋 Docker Compose: $(command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1 && echo "${GREEN}Disponível${NC}" || echo "${RED}Não disponível${NC}")"
    echo -e "💾 Logs: $(ls "$LOG_DIR"/*.log 2>/dev/null | wc -l) arquivos"
    echo -e "📦 Backups: $(ls "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l) arquivos"

    if [ "$DOCKER_ACTIVE" = true ]; then
        local container_count
        container_count=$(docker ps -q 2>/dev/null | wc -l)
        echo -e "🧩 Containers ativos: $container_count"
    fi

    pause
}

pause() {
    if [ "$AUTO_REFRESH" = false ]; then
        echo -e "\n${DIM}Pressione Enter para continuar...${NC}"
        read -r
    else
        echo -e "\n${DIM}Atualizando em $MONITOR_INTERVAL segundos...${NC}"
        sleep "$MONITOR_INTERVAL"
    fi
}

# ============================================================================
# FUNÇÃO PRINCIPAL DE MENU
# ============================================================================

main_menu() {
    detect_environment

    while true; do
        local choice

        if [ "$USE_WHIPTAIL" = true ]; then
            choice=$(show_main_menu_whiptail)
        else
            show_main_menu_text
            read -r choice
        fi

        case "$choice" in
            1)
                if [ "$USE_WHIPTAIL" = true ]; then
                    show_containers_whiptail
                else
                    show_containers_text
                fi
                ;;
            2)
                if [ "$USE_WHIPTAIL" = true ]; then
                    show_logs_whiptail
                else
                    show_logs_text
                fi
                ;;
            3)
                if [ "$USE_WHIPTAIL" = true ]; then
                    show_system_usage_whiptail
                else
                    show_system_usage_text
                fi
                ;;
            4)
                if [ "$USE_WHIPTAIL" = true ]; then
                    show_backups_whiptail
                else
                    show_backups_text
                fi
                ;;
            5)
                if [ "$USE_WHIPTAIL" = true ]; then
                    show_system_status_whiptail
                else
                    show_system_status_text
                fi
                ;;
            6)
                configure_settings
                ;;
            7|"")
                echo -e "\n${GREEN}${SUCCESS} Saindo do SILA System Monitor...${NC}"
                exit 0
                ;;
            *)
                if [ "$USE_WHIPTAIL" = false ]; then
                    echo -e "\n${YELLOW}${WARNING} Opção inválida: $choice${NC}"
                    pause
                fi
                ;;
        esac
    done
}

# ============================================================================
# CONFIGURAÇÕES DO SISTEMA
# ============================================================================

configure_settings() {
    if [ "$USE_WHIPTAIL" = true ]; then
        local choice
        choice=$(whiptail --title "Configurações" --menu "Escolha uma configuração:" 15 50 4 \
            "1" "Toggle refresh automático ($AUTO_REFRESH)" \
            "2" "Alterar intervalo de refresh ($MONITOR_INTERVAL)" \
            "3" "Ver informações do sistema" \
            "4" "Voltar" \
            3>&1 1>&2 2>&3)

        case "$choice" in
            1)
                AUTO_REFRESH=$([ "$AUTO_REFRESH" = true ] && echo false || echo true)
                whiptail --msgbox "Refresh automático: $AUTO_REFRESH" 8 40
                ;;
            2)
                local new_interval
                new_interval=$(whiptail --inputbox "Novo intervalo (segundos):" 8 40 "$MONITOR_INTERVAL" 3>&1 1>&2 2>&3)
                if [[ "$new_interval" =~ ^[0-9]+$ ]] && [ "$new_interval" -gt 0 ]; then
                    MONITOR_INTERVAL="$new_interval"
                    whiptail --msgbox "Intervalo alterado para $MONITOR_INTERVAL segundos" 8 50
                else
                    whiptail --msgbox "Valor inválido!" 8 30
                fi
                ;;
            3)
                whiptail --msgbox "SILA System Monitor v2.0\nDiretório: $ENV_DIR\nLogs: $LOG_DIR\nBackups: $BACKUP_DIR" 10 50
                ;;
        esac
    else
        echo -e "\n${GEAR} ${BOLD}Configurações:${NC}\n"
        echo -e "1. Toggle refresh automático (atual: $AUTO_REFRESH)"
        echo -e "2. Alterar intervalo de refresh (atual: $MONITOR_INTERVAL)"
        echo -e "3. Ver informações do sistema"
        echo -e "4. Voltar"
        echo ""
        echo -n "Escolha uma opção [1-4]: "
        read -r choice

        case "$choice" in
            1)
                AUTO_REFRESH=$([ "$AUTO_REFRESH" = true ] && echo false || echo true)
                echo -e "${GREEN}Refresh automático: $AUTO_REFRESH${NC}"
                ;;
            2)
                echo -n "Novo intervalo (segundos): "
                read -r new_interval
                if [[ "$new_interval" =~ ^[0-9]+$ ]] && [ "$new_interval" -gt 0 ]; then
                    MONITOR_INTERVAL="$new_interval"
                    echo -e "${GREEN}Intervalo alterado para $MONITOR_INTERVAL segundos${NC}"
                else
                    echo -e "${RED}Valor inválido!${NC}"
                fi
                ;;
            3)
                echo -e "📋 Informações do Sistema:"
                echo -e "Versão: SILA System Monitor v2.0"
                echo -e "Diretório: $ENV_DIR"
                echo -e "Logs: $LOG_DIR"
                echo -e "Backups: $BACKUP_DIR"
                ;;
        esac
        pause
    fi
}

# Parse de argumentos para funcionalidades avançadas
ENV_FILTER=""
REALTIME_MODE=false
EXPORT_METRICS=false
EXPORT_JSON=false
EXPORT_MD=false
NOTIFICATION_TEST=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --env=*)
            ENV_FILTER="${1#*=}"
            shift
            ;;
        --realtime)
            REALTIME_MODE=true
            shift
            ;;
        --export)
            EXPORT_METRICS=true
            EXPORT_JSON=true
            shift
            ;;
        --export-json)
            EXPORT_JSON=true
            shift
            ;;
        --export-md)
            EXPORT_MD=true
            shift
            ;;
        --notify-test)
            NOTIFICATION_TEST=true
            shift
            ;;
        --help)
            echo "Uso: $0 [OPÇÕES]"
            echo ""
            echo "OPÇÕES:"
            echo "  --env=AMBIENTE    Filtrar por ambiente (dev/staging/prod)"
            echo "  --realtime       Modo monitoramento em tempo real"
            echo "  --export         Exportar métricas (stdout) e snapshot JSON"
            echo "  --export-json    Exportar snapshot em JSON para reports/monitoring"
            echo "  --export-md      Exportar snapshot em Markdown para reports/monitoring"
            echo "  --notify-test    Testar notificações"
            echo "  --help           Mostra esta ajuda"
            echo ""
            echo "EXEMPLOS:"
            echo "  $0                      # Interface interativa"
            echo "  $0 --env=prod          # Mostrar apenas ambiente produção"
            echo "  $0 --realtime          # Monitoramento contínuo"
            echo "  $0 --export-json       # Gera JSON em reports/monitoring"
            echo "  $0 --export-md         # Gera Markdown em reports/monitoring"
            exit 0
            ;;
        *)
            echo "❌ Opção desconhecida: $1"
            echo "Use --help para ver as opções disponíveis"
            exit 1
            ;;
    esac
done

collect_basic_status() {
    detect_environment

    SNAP_TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    SNAP_ENV_DIR="$ENV_DIR"
    SNAP_PROJECT_ROOT="$PROJECT_ROOT"

    if command -v docker >/dev/null 2>&1; then
        SNAP_DOCKER_AVAILABLE=true
        SNAP_CONTAINER_COUNT="$(docker ps -q 2>/dev/null | wc -l | tr -d ' ')"
    else
        SNAP_DOCKER_AVAILABLE=false
        SNAP_CONTAINER_COUNT=0
    fi

    if command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1; then
        SNAP_COMPOSE_AVAILABLE=true
    else
        SNAP_COMPOSE_AVAILABLE=false
    fi

    if [[ -d "$LOG_DIR" ]]; then
        SNAP_LOG_FILES="$(ls "$LOG_DIR"/*.log 2>/dev/null | wc -l | tr -d ' ')"
    else
        SNAP_LOG_FILES=0
    fi

    if [[ -d "$BACKUP_DIR" ]]; then
        SNAP_BACKUP_FILES="$(ls "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l | tr -d ' ')"
    else
        SNAP_BACKUP_FILES=0
    fi

    [[ -d "$PROJECT_ROOT/apps/backend" ]] && SNAP_BACKEND_PRESENT=true || SNAP_BACKEND_PRESENT=false
    [[ -d "$PROJECT_ROOT/apps/frontend" ]] && SNAP_FRONTEND_PRESENT=true || SNAP_FRONTEND_PRESENT=false
}

export_json_report() {
    mkdir -p "$REPORT_DIR"
    local outfile="$REPORT_DIR/monitor_$(date -u +%Y%m%dT%H%M%SZ).json"
    cat > "$outfile" << EOF
{
  "timestamp": "$SNAP_TIMESTAMP",
  "environment_dir": "$SNAP_ENV_DIR",
  "project_root": "$SNAP_PROJECT_ROOT",
  "docker_available": $SNAP_DOCKER_AVAILABLE,
  "docker_compose_available": $SNAP_COMPOSE_AVAILABLE,
  "container_count": $SNAP_CONTAINER_COUNT,
  "log_files": $SNAP_LOG_FILES,
  "backup_files": $SNAP_BACKUP_FILES,
  "apps_backend_present": $SNAP_BACKEND_PRESENT,
  "apps_frontend_present": $SNAP_FRONTEND_PRESENT
}
EOF
    echo "JSON gerado em: $outfile"
}

export_md_report() {
    mkdir -p "$REPORT_DIR"
    local outfile="$REPORT_DIR/monitor_$(date -u +%Y%m%dT%H%M%SZ).md"
    cat > "$outfile" << EOF
# SILA System - Snapshot de Monitorização

- Timestamp: $SNAP_TIMESTAMP
- Diretório de ambiente: $SNAP_ENV_DIR
- Raiz do projeto: $SNAP_PROJECT_ROOT
- Docker disponível: $SNAP_DOCKER_AVAILABLE
- Docker Compose disponível: $SNAP_COMPOSE_AVAILABLE
- Containers ativos: $SNAP_CONTAINER_COUNT
- Arquivos de log: $SNAP_LOG_FILES
- Arquivos de backup: $SNAP_BACKUP_FILES
- apps/backend presente: $SNAP_BACKEND_PRESENT
- apps/frontend presente: $SNAP_FRONTEND_PRESENT

EOF
    echo "Markdown gerado em: $outfile"
}

# Se estiver em modo de exportação, gerar snapshot e sair
if [ "$EXPORT_JSON" = true ] || [ "$EXPORT_MD" = true ] || [ "$EXPORT_METRICS" = true ]; then
    collect_basic_status
    if [ "$EXPORT_JSON" = true ]; then
        export_json_report
    fi
    if [ "$EXPORT_MD" = true ]; then
        export_md_report
    fi
    if [ "$EXPORT_METRICS" = true ]; then
        echo "timestamp=$SNAP_TIMESTAMP"
        echo "env_dir=$SNAP_ENV_DIR"
        echo "project_root=$SNAP_PROJECT_ROOT"
        echo "docker_available=$SNAP_DOCKER_AVAILABLE"
        echo "docker_compose_available=$SNAP_COMPOSE_AVAILABLE"
        echo "container_count=$SNAP_CONTAINER_COUNT"
        echo "log_files=$SNAP_LOG_FILES"
        echo "backup_files=$SNAP_BACKUP_FILES"
    fi
    exit 0
fi

# Aplicar configurações de interface
if [ "$USE_WHIPTAIL" = true ]; then
    choice=$(whiptail --title "Configurações Iniciais" --menu "Interface detectada: Whiptail" 12 50 3 \
        "1" "Interface gráfica (recomendado)" \
        "2" "Interface de texto" \
        "3" "Sair" \
        3>&1 1>&2 2>&3)

    case "$choice" in
        1) USE_WHIPTAIL=true ;;
        2) USE_WHIPTAIL=false ;;
        3) exit 0 ;;
    esac
fi

# Iniciar monitoramento
main_menu
