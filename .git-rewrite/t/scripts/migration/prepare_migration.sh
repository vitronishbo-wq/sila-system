#!/bin/bash

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

# Aliases para compatibilidade
warning() {
    warn "$1"
}

# Verifica e prepara ambiente para migração
prepare_migration_env() {
    log "🔍 Preparando ambiente para migração..."

    # 1. Criar diretório de backups
    mkdir -p backups

    # 2. Verificar/criar diretório de logs
    mkdir -p logs

    # 3. Instalar dependências Python necessárias
    log "📦 Instalando dependências Python..."
    source .venv/bin/activate 2>/dev/null || python3 -m venv .venv && source .venv/bin/activate
    pip install --no-cache-dir bcrypt psycopg2-binary python-dotenv
    success "✅ Dependências instaladas"

    # 4. Verificar conexão com banco
    log "🔌 Verificando conexão com banco de dados..."
    python3 -c "
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', 'postgres'),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        Truman1*Marcelo1*POSTGRES_PASSWORD', 'postgres'),
        host='localhost',
        port=5432
    )
    conn.close()
    print('Conexão OK')
except Exception as e:
    print(f'Erro: {str(e)}')
    exit(1)
"

    if [ $? -eq 0 ]; then
        success "✅ Conexão com banco de dados estabelecida"
    else
        error "❌ Falha na conexão com banco de dados"
        exit 1
    fi

    # 5. Verificar variáveis de ambiente críticas
    log "🔐 Verificando variáveis de ambiente críticas..."
    critical_vars=(
        "AUTH_SECRET_KEY"
        "PASSWORD_HASH_ALGORITHM"
        "PASSWORD_HASH_ROUNDS"
        "ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    missing_vars=()
    source .env 2>/dev/null || true

    for var in "${critical_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=($var)
        fi
    done

    if [ ${#missing_vars[@]} -ne 0 ]; then
        warning "⚠️ Variáveis de ambiente faltando: ${missing_vars[*]}"
        warning "Executando fix_auth_env.sh para corrigir..."
        ./fix_auth_env.sh
    else
        success "✅ Todas as variáveis críticas encontradas"
    fi
}

# Função principal
main() {
    log "🚀 Iniciando preparação do ambiente de migração..."

    # Executar preparação
    prepare_migration_env

    success "🎉 Ambiente de migração preparado com sucesso!"
    log "Você pode agora executar o script de migração com:"
    log "ENVIRONMENT=development ./execute_auth_migration.sh"
}

# Executar script
main
