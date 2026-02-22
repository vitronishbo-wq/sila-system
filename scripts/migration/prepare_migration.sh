#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

prepare_migration_env() {
    log "🔍 Preparando ambiente para migração..."

    mkdir -p backups
    mkdir -p logs

    log "📦 Configurando ambiente virtual e dependências..."
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install --no-cache-dir bcrypt psycopg2-binary python-dotenv sqlalchemy asyncpg
    
    log "🔌 Verificando conexão com banco de dados Docker..."
    python3 - <<'PY'
import psycopg2
import os
import sys

try:
    conn = psycopg2.connect(
        dbname="sila_db",
        user="sila_user",
        password="Trumanmarcelo_1983",
        host="localhost",
        port=5434
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f"Erro: {e}")
    sys.exit(1)
PY

    if [ $? -eq 0 ]; then
        success "✅ Conexão estabelecida (Porta 5434)"
    else
        error "❌ Falha na conexão. Certifique-se que o container 'db' está rodando."
        exit 1
    fi

    log "🔐 Validando credenciais no .env..."
    if [[ ! -f ".env" ]]; then
        error ".env não encontrado"
        exit 1
    fi
    
    export POSTGRES_PASSWORD=Trumanmarcelo_1983
    export DATABASE_URL="postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_db"
}

main() {
    prepare_migration_env
    success "🎉 Ambiente pronto!"
    log "Próximo passo: ./execute_auth_migration.sh"
}

main