#!/bin/bash

# ===========================================
# SILA Backend Fix Script
# ===========================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

cd "$(dirname "$0")/.." || exit 1

log_info "🔧 Corrigindo Backend..."

# Verificar e adicionar dependências críticas
REQUIREMENTS_FILE="backend/requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    # Verificar passlib
    if ! grep -q "passlib\[bcrypt\]" "$REQUIREMENTS_FILE"; then
        echo "passlib[bcrypt]==1.7.4" >> "$REQUIREMENTS_FILE"
        log_success "passlib[bcrypt] adicionado"
    fi

    # Verificar alembic
    if ! grep -q "alembic" "$REQUIREMENTS_FILE"; then
        echo "alembic>=1.8.0" >> "$REQUIREMENTS_FILE"
        log_success "alembic adicionado"
    fi

    # Verificar uvicorn
    if ! grep -q "uvicorn" "$REQUIREMENTS_FILE"; then
        echo "uvicorn[standard]>=0.18.0" >> "$REQUIREMENTS_FILE"
        log_success "uvicorn adicionado"
    fi

    log_success "Dependências do backend verificadas"
else
    log_warning "requirements.txt não encontrado"
fi

# Verificar estrutura do backend
if [ -f "backend/main.py" ]; then
    log_success "main.py encontrado"
else
    log_warning "main.py não encontrado"
fi

if [ -f "backend/entrypoint.sh" ]; then
    chmod +x backend/entrypoint.sh
    log_success "entrypoint.sh executável"
fi

log_success "🎉 Backend fix concluído!"
