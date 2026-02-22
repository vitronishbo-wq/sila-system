#!/bin/bash

# ============================================================================
# SILA SYSTEM - INSTALADOR E NORMALIZADOR DE AMBIENTE
# ============================================================================
# Este script automatiza a configuração completa do ambiente de desenvolvimento,
# incluindo a instalação de dependências do backend e frontend, e prepara
# o terreno para a normalização automática de bibliotecas.
# ============================================================================

set -euo pipefail

# --- Configurações e Cores ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# Cores para a saída
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Funções de Logging ---
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# --- Funções de Verificação ---
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "Comando '$1' não encontrado. Por favor, instale-o antes de continuar."
    fi
}

# --- Funções de Instalação ---

install_backend_deps() {
    log_info "Iniciando instalação das dependências do Backend (Python)..."

    # 1. Criar ambiente virtual
    if [ ! -d "$PROJECT_ROOT/.venv" ]; then
        log_info "Criando ambiente virtual em .venv..."
        python3 -m venv "$PROJECT_ROOT/.venv"
    else
        log_info "Ambiente virtual .venv já existe."
    fi

    # 2. Ativar VENV e instalar dependências
    source "$PROJECT_ROOT/.venv/bin/activate"

    log_info "Atualizando pip..."
    pip install --upgrade pip

    log_info "Instalando dependências de 'requirements.txt'..."
    if pip install -r "$PROJECT_ROOT/requirements.txt"; then
        log_success "Dependências do Backend instaladas com sucesso."
    else
        log_error "Falha ao instalar as dependências do Backend."
    fi

    deactivate
}

install_frontend_deps() {
    log_info "Iniciando instalação das dependências do Frontend (Node.js)..."
    local frontend_dir="$PROJECT_ROOT/frontend"

    if [ ! -d "$frontend_dir" ]; then
        log_warn "Diretório do Frontend ('$frontend_dir') não encontrado. Pulando instalação."
        return
    fi

    if [ ! -f "$frontend_dir/package.json" ]; then
        log_warn "'package.json' não encontrado em '$frontend_dir'. Pulando instalação."
        return
    fi

    log_info "Navegando para o diretório do frontend e executando 'npm install'..."
    if (cd "$frontend_dir" && npm install); then
        log_success "Dependências do Frontend instaladas com sucesso."
    else
        log_error "Falha ao instalar as dependências do Frontend."
    fi
}

# --- Funções de Normalização (Placeholders) ---

normalize_dependencies() {
    log_info "(Placeholder) Iniciando varredura e normalização de dependências..."
    # Futura implementação: analisar requirements.txt, package.json, etc.,
    # e garantir que as versões estão padronizadas em todo o projeto.
    log_success "(Placeholder) Normalização de dependências concluída."
}


# --- Função Principal ---

main() {
    log_info "🚀 Iniciando o Configurador Automático do Ambiente SILA..."

    # 1. Verificar ferramentas essenciais
    log_info "Verificando ferramentas essenciais..."
    check_command python3
    check_command pip
    check_command npm
    log_success "Todas as ferramentas essenciais foram encontradas."

    # 2. Instalar dependências
    install_backend_deps
    install_frontend_deps

    # 3. Normalizar dependências (atualmente um placeholder)
    normalize_dependencies

    echo
    log_success "🎉 Ambiente de desenvolvimento SILA configurado com sucesso!"
    log_info "O ambiente virtual '.venv' está pronto para ser ativado."
}

# --- Ponto de Entrada ---
main "$@"
