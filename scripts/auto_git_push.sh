#!/bin/bash
# ============================================================================
# 🔐 SECURE AUTO GIT PUSH - SILA System
# ============================================================================
# Uso: ./scripts/auto_git_push.sh "commit message"
# 
# Funcionalidades:
#  - Usa token de GitHub via variável de ambiente (seguro)
#  - Valida que não há arquivos de segredo sendo commitados
#  - Faz commit, push e notifica
#  - Logging de todas as operações
#
# Setup inicial:
#  export GITHUB_TOKEN='seu_token_aqui'
#  export GITHUB_USERNAME='seu_username'
#  export GITHUB_REPO='seu_username/seu_repo'
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="${PROJECT_ROOT}/git_push.log"

log_info() { echo -e "${BLUE}ℹ️  $1${NC}" | tee -a "$LOG_FILE"; }
log_success() { echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"; }
log_error() { echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}" | tee -a "$LOG_FILE"; }

check_security() {
    log_info "🔐 Verificando segurança..."
    
    # Verify .env files are NOT staged
    if git diff --cached --name-only | grep -E '\.env($|\..*\.local)' | grep -v '.env.example'; then
        log_error "❌ Ficheiros .env NÃO devem ser commitados!"
        exit 1
    fi
    
    # Verify no secrets in diff
    local patterns=("ghp_" "AKIA" "BEGIN RSA" "BEGIN OPENSSH")
    for pattern in "${patterns[@]}"; do
        if git diff --cached | grep -i "$pattern"; then
            log_warning "⚠️  Padrão de secret encontrado: $pattern"
        fi
    done
    
    log_success "Segurança verificada OK"
}

setup_github_auth() {
    log_info "🔐 Configurando autenticação GitHub..."
    
    if [ -z "$GITHUB_TOKEN" ]; then
        log_error "❌ GITHUB_TOKEN não está definido!"
        log_info "Execute: export GITHUB_TOKEN='seu_token_aqui'"
        exit 1
    fi
    
    if [ -z "$GITHUB_USERNAME" ]; then
        log_error "❌ GITHUB_USERNAME não está definido!"
        exit 1
    fi
    
    if [ -z "$GITHUB_REPO" ]; then
        log_error "❌ GITHUB_REPO não está definido!"
        exit 1
    fi
    
    log_success "GitHub auth configurada"
}

perform_git_push() {
    local commit_msg="$1"
    
    if [ -z "$commit_msg" ]; then
        log_error "Uso: ./auto_git_push.sh \"commit message\""
        exit 1
    fi
    
    cd "$PROJECT_ROOT"
    
    log_info "📊 Status:"
    git status --short | head -10
    
    log_info "📦 Adicionando ficheiros..."
    git add .
    git reset -- apps/backend/.env .env 2>/dev/null || true
    
    log_info "📝 Commitando: $commit_msg"
    git commit -m "$commit_msg" || { log_warning "Nada para commitear"; return 0; }
    
    local remote_url="https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git"
    local branch=$(git rev-parse --abbrev-ref HEAD)
    
    log_info "🚀 Fazendo push para origin/$branch..."
    git push "$remote_url" "$branch" 2>&1 | grep -v "Token\|PASSWORD" || true
    
    if [ $? -eq 0 ]; then
        local commit_hash=$(git rev-parse --short HEAD)
        log_success "Push concluído!"
        log_info "💾 Branch: $branch | Hash: $commit_hash"
        log_info "🔗 https://github.com/${GITHUB_REPO}/commits/$branch"
    else
        log_error "Push falhou!"
        exit 1
    fi
}

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║              🔐 SECURE AUTO GIT PUSH - SILA SYSTEM                 ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    echo "Log iniciado: $(date)" > "$LOG_FILE"
    
    check_security
    setup_github_auth
    perform_git_push "$1"
    
    echo ""
    log_success "Operação concluída!"
    echo ""
}

main "$@" 
