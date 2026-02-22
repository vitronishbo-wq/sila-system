#!/bin/bash

################################################################################
# BIBLIOTECA CENTRALIZADA DE CORES
# Definições de cores ANSI para todos os scripts SILA
#
# Uso:
#   source "$(dirname "$0")/../lib/colors.sh"
#   echo -e "${RED}Texto em vermelho${NC}"
#   echo -e "${GREEN}Texto em verde${NC}"
################################################################################

# ============================================================================
# CORES BÁSICAS
# ============================================================================

RED='\033[0;31m'           # Vermelho
GREEN='\033[0;32m'         # Verde
BLUE='\033[0;34m'          # Azul
YELLOW='\033[1;33m'        # Amarelo
CYAN='\033[0;36m'          # Ciano
MAGENTA='\033[0;35m'       # Magenta
WHITE='\033[0;37m'         # Branco
BLACK='\033[0;30m'         # Preto

# ============================================================================
# ESTILOS
# ============================================================================

BOLD='\033[1m'             # Negrito
DIM='\033[2m'              # Escuro
ITALIC='\033[3m'           # Itálico
UNDERLINE='\033[4m'        # Sublinhado
BLINK='\033[5m'            # Piscante
REVERSE='\033[7m'          # Invertido
HIDDEN='\033[8m'           # Oculto
STRIKETHROUGH='\033[9m'    # Riscado

# Reset
NC='\033[0m'               # Sem cor (reset)

# ============================================================================
# COMBINAÇÕES ÚTEIS
# ============================================================================

# Cores com negrito
BOLD_RED="\033[1;31m"
BOLD_GREEN="\033[1;32m"
BOLD_BLUE="\033[1;34m"
BOLD_YELLOW="\033[1;33m"
BOLD_CYAN="\033[1;36m"
BOLD_MAGENTA="\033[1;35m"
BOLD_WHITE="\033[1;37m"

# Cores de fundo
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_BLUE='\033[44m'
BG_YELLOW='\033[43m'
BG_CYAN='\033[46m'
BG_MAGENTA='\033[45m'
BG_WHITE='\033[47m'

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

# Desabilitar cores (para output em ficheiros)
disable_colors() {
    RED=''
    GREEN=''
    BLUE=''
    YELLOW=''
    CYAN=''
    MAGENTA=''
    WHITE=''
    BLACK=''
    BOLD=''
    DIM=''
    ITALIC=''
    UNDERLINE=''
    BLINK=''
    REVERSE=''
    HIDDEN=''
    STRIKETHROUGH=''
    NC=''
    BOLD_RED=''
    BOLD_GREEN=''
    BOLD_BLUE=''
    BOLD_YELLOW=''
    BOLD_CYAN=''
    BOLD_MAGENTA=''
    BOLD_WHITE=''
    BG_RED=''
    BG_GREEN=''
    BG_BLUE=''
    BG_YELLOW=''
    BG_CYAN=''
    BG_MAGENTA=''
    BG_WHITE=''
}

# Habilitar cores (padrão)
enable_colors() {
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    YELLOW='\033[1;33m'
    CYAN='\033[0;36m'
    MAGENTA='\033[0;35m'
    WHITE='\033[0;37m'
    BLACK='\033[0;30m'
    BOLD='\033[1m'
    DIM='\033[2m'
    ITALIC='\033[3m'
    UNDERLINE='\033[4m'
    BLINK='\033[5m'
    REVERSE='\033[7m'
    HIDDEN='\033[8m'
    STRIKETHROUGH='\033[9m'
    NC='\033[0m'
    BOLD_RED="\033[1;31m"
    BOLD_GREEN="\033[1;32m"
    BOLD_BLUE="\033[1;34m"
    BOLD_YELLOW="\033[1;33m"
    BOLD_CYAN="\033[1;36m"
    BOLD_MAGENTA="\033[1;35m"
    BOLD_WHITE="\033[1;37m"
    BG_RED='\033[41m'
    BG_GREEN='\033[42m'
    BG_BLUE='\033[44m'
    BG_YELLOW='\033[43m'
    BG_CYAN='\033[46m'
    BG_MAGENTA='\033[45m'
    BG_WHITE='\033[47m'
}

# Detectar se terminal suporta cores
supports_colors() {
    if [ -t 1 ]; then
        return 0  # Terminal interativo, suporta cores
    else
        return 1  # Não é terminal interativo
    fi
}

# Auto-detectar e aplicar cores
if ! supports_colors; then
    disable_colors
fi

################################################################################
# FIM DA BIBLIOTECA
################################################################################
