#!/bin/bash
# ============================================================================
# 🔐 SECURE DEVELOPMENT ENVIRONMENT SETUP
# ============================================================================
# Setup local .env files from templates
# - Prompts para valores sensíveis (nunca commitear)
# - Configura variáveis de GitHub para auto_git_push.sh
# - Implementa secrets management
#
# Uso: ./setup_dev_env.sh
# ============================================================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# ============================================================================
# SETUP BACKEND .env
# ============================================================================

setup_backend_env() {
    local EXAMPLE=apps/backend/.env.example
    local TARGET=apps/backend/.env
    
    if [ ! -f "$EXAMPLE" ]; then
        log_error "Ficheiro não encontrado: $EXAMPLE"
        exit 1
    fi
    
    if [ -f "$TARGET" ]; then
        log_warning "$TARGET já existe"
        read -p "Sobrescrever? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 0
        fi
    fi
    
    log_info "Configurando Backend .env..."
    cp "$EXAMPLE" "$TARGET"
    
    # Database
    if grep -q "REPLACE_WITH_DATABASE_PASSWORD" "$TARGET"; then
        read -s -p "🔐 Database password: " DB_PASS
        echo
        sed -i "s/REPLACE_WITH_DATABASE_PASSWORD/${DB_PASS//\//\\/}/g" "$TARGET"
        log_success "Database password configurada"
    fi
    
    # SECRET_KEY
    if grep -q "REPLACE_WITH_SECRET_KEY" "$TARGET"; then
        read -s -p "🔐 SECRET_KEY (JWT): " SK
        echo
        sed -i "s/REPLACE_WITH_SECRET_KEY/${SK//\//\\/}/g" "$TARGET"
        log_success "SECRET_KEY configurada"
    fi
    
    chmod 600 "$TARGET"
    log_success "✓ $TARGET criado (chmod 600)"
}

# ============================================================================
# SETUP GITHUB CREDENTIALS
# ============================================================================

setup_github_credentials() {
    log_info "Configurando GitHub credentials para push automático..."
    
    local GITHUB_CONFIG="$HOME/.github_credentials"
    
    if [ -f "$GITHUB_CONFIG" ]; then
        log_warning "$GITHUB_CONFIG já existe"
        read -p "Reconfigurar? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 0
        fi
    fi
    
    # GitHub Token
    log_info "🔐 Configure seu GitHub Token:"
    log_info "   1. Ir para: https://github.com/settings/tokens/new"
    log_info "   2. Selecionar: repo, workflow"
    log_info "   3. Copiar token (aparece apenas uma vez!)"
    read -s -p "GitHub Token: " GITHUB_TOKEN
    echo
    
    # GitHub Username
    read -p "GitHub Username: " GITHUB_USERNAME
    
    # GitHub Repository
    read -p "GitHub Repository (username/repo): " GITHUB_REPO
    
    # Save to credentials file
    cat > "$GITHUB_CONFIG" << EOF
#!/bin/bash
# GitHub Credentials (NÃO COMETER!)
export GITHUB_TOKEN='${GITHUB_TOKEN}'
export GITHUB_USERNAME='${GITHUB_USERNAME}'
export GITHUB_REPO='${GITHUB_REPO}'
EOF
    
    chmod 600 "$GITHUB_CONFIG"
    log_success "✓ GitHub credentials salvos em $GITHUB_CONFIG (chmod 600)"
    
    log_info ""
    log_info "Para usar em futuras sessões, execute:"
    log_info "  source $GITHUB_CONFIG"
}

# ============================================================================
# SETUP SECRETS MANAGEMENT
# ============================================================================

setup_secrets_management() {
    log_info "Implementando Secrets Management..."
    
    # Create .secrets directory
    mkdir -p ".secrets"
    chmod 700 ".secrets"
    
    cat > .secrets/README.md << 'EOF'
# 🔐 Secrets Management

Este diretório contém configurations para gestão segura de segredos.

## AWS Secrets Manager

```bash
aws secretsmanager create-secret \
  --name sila/backend/db-password \
  --secret-string 'password_here'
```

## HashiCorp Vault

```bash
vault kv put secret/sila/backend \
  db_password="password"
```

## Local Development

Para desenvolvimento local, use:
- `.env` (gitignored)
- `~/.github_credentials` (gitignored)
- Variáveis de ambiente

NUNCA commitar ficheiros de segredos!
EOF
    
    log_success "✓ Diretório .secrets criado com documentação"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║           🔐 SECURE DEVELOPMENT ENVIRONMENT SETUP                  ║"
    echo "║                      SILA System                                   ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Step 1: Backend .env
    setup_backend_env
    echo ""
    
    # Step 2: GitHub Credentials
    read -p "Configurar GitHub para push automático? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_github_credentials
    fi
    echo ""
    
    # Step 3: Secrets Management
    setup_secrets_management
    echo ""
    
    # Summary
    echo "╔════════════════════════════════════════════════════════════════════╗"
    log_success "Setup concluído!"
    echo ""
    log_info "✅ Próximos passos:"
    echo "   1. Carregar variáveis de ambiente:"
    echo "      source $HOME/.github_credentials  (se configurado)"
    echo ""
    echo "   2. Iniciar desenvolvimento:"
    echo "      cd apps/backend"
    echo "      python -m uvicorn app.main:app --reload"
    echo ""
    echo "   3. Para push automático seguro:"
    echo "      ./scripts/auto_git_push.sh \"sua mensagem de commit\""
    echo ""
    echo "   4. Revisar documentação de segurança:"
    echo "      cat SECURITY_ALERT.md"
    echo ""
    echo "🔐 LEMBRE-SE:"
    echo "   - NUNCA commitar .env ou credentials"
    echo "   - SEMPRE usar variáveis de ambiente em produção"
    echo "   - Rotacionar tokens regularmente"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
}

main "$@"
