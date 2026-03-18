#!/bin/bash

################################################################################
# BIBLIOTECA CENTRALIZADA DE LOGGING
# Funções comuns de logging para todos os scripts SILA
#
# Uso:
#   source "$(dirname "$0")/../lib/logging.sh"
#   log "Mensagem de informação"
#   success "Operação bem-sucedida"
#   error "Erro encontrado"
#   warn "Aviso importante"
#   info "Informação adicional"
################################################################################

# Cores (importadas de colors.sh se disponível)
if [ -f "$(dirname "${BASH_SOURCE[0]}")/colors.sh" ]; then
    source "$(dirname "${BASH_SOURCE[0]}")/colors.sh"
else
    # Fallback se colors.sh não estiver disponível
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    YELLOW='\033[1;33m'
    CYAN='\033[0;36m'
    MAGENTA='\033[0;35m'
    BOLD='\033[1m'
    NC='\033[0m'
fi

# ============================================================================
# FUNÇÕES DE LOGGING
# ============================================================================

# Log genérico com timestamp
log() {
    echo "$(date +'%H:%M:%S') [LOG] $*"
}

# Mensagem de sucesso
success() {
    echo -e "${GREEN}✅ $*${NC}"
}

# Mensagem de erro
error() {
    echo -e "${RED}❌ $*${NC}" >&2
}

# Mensagem de aviso
warn() {
    echo -e "${YELLOW}⚠️  $*${NC}"
}

# Mensagem de informação
info() {
    echo -e "${BLUE}ℹ️  $*${NC}"
}

# Mensagem de seção/header
section() {
    echo -e "\n${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}▶ $*${NC}"
    echo -e "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# Log com nível (compatível com sila_start.sh)
log_level() {
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
            echo -e "[${timestamp}] ${RED}[ERROR]${NC} $message" >&2
            ;;
        FATAL)
            echo -e "[${timestamp}] ${RED}[FATAL]${NC} $message" >&2
            ;;
        *)
            echo -e "[${timestamp}] [${level}] $message"
            ;;
    esac
}

# Aliases para compatibilidade
log_info() { log_level INFO "$1"; }
log_success() { log_level SUCCESS "$1"; }
log_warn() { log_level WARN "$1"; }
log_error() { log_level ERROR "$1"; }
log_fatal() { log_level FATAL "$1"; }

# ============================================================================
# FUNÇÕES DE LOGGING COM ARQUIVO
# ============================================================================

# Inicializar arquivo de log
init_log_file() {
    local log_file="$1"
    local script_name="${2:-$(basename "$0")}"

    mkdir -p "$(dirname "$log_file")"

    {
        echo "================================================================================"
        echo "Log iniciado: $(date)"
        echo "Script: $script_name"
        echo "================================================================================"
    } >> "$log_file"
}

# Log para arquivo e console
log_to_file() {
    local log_file="$1"
    local message="$2"
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')

    echo "[${timestamp}] $message" | tee -a "$log_file"
}

# ============================================================================
# FUNÇÕES DE VALIDAÇÃO COM LOG
# ============================================================================

# Verificar se comando existe
require_command() {
    local cmd="$1"

    if ! command -v "$cmd" &> /dev/null; then
        error "Comando obrigatório não encontrado: $cmd"
        return 1
    fi
    return 0
}

# Verificar se arquivo existe
require_file() {
    local file="$1"

    if [ ! -f "$file" ]; then
        error "Arquivo obrigatório não encontrado: $file"
        return 1
    fi
    return 0
}

# Verificar se diretório existe
require_dir() {
    local dir="$1"

    if [ ! -d "$dir" ]; then
        error "Diretório obrigatório não encontrado: $dir"
        return 1
    fi
    return 0
}

# ============================================================================
# FUNÇÕES DE PROGRESSO
# ============================================================================

# Spinner simples
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'

    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Barra de progresso
progress_bar() {
    local current=$1
    local total=$2
    local width=50

    local percent=$((current * 100 / total))
    local filled=$((percent * width / 100))

    printf "\r["
    printf "%${filled}s" | tr ' ' '='
    printf "%$((width - filled))s" | tr ' ' '-'
    printf "] %d%%" "$percent"
}

################################################################################
# FIM DA BIBLIOTECA
################################################################################
