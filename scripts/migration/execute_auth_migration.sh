#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

export POSTGRES_PASSWORD=Trumanmarcelo_1983
export DATABASE_URL="postgresql+asyncpg://sila_user:Trumanmarcelo_1983@db:5432/sila_db"
export DOCKER_COMPOSE_FILE="docker-compose.yml"

check_status() {
    if [ $? -eq 0 ]; then
        success "$1"
    else
        error "$1 falhou!"
        exit 1
    fi
}

log "🧹 Limpando ambiente Docker..."
docker compose down --remove-orphans 2>/dev/null || true

log "🚀 Iniciando Banco de Dados para migração..."
docker compose up -d db

log "⏳ Aguardando PostgreSQL..."
for i in {1..30}; do
    if docker compose exec -T db pg_isready -U sila_user >/dev/null 2>&1; then
        log "✅ PostgreSQL pronto!"
        break
    fi
    sleep 2
done

log "📦 Criando backup preventivo..."
mkdir -p backups
BACKUP_FILE="backups/db_before_auth_mig_$(date +%Y%m%d_%H%M%S).sql"
docker compose exec -T db pg_dump -U sila_user sila_db > "$BACKUP_FILE"
check_status "Backup"

log "🔧 Preparando ambiente Python..."
python3 -m venv .venv --clear
source .venv/bin/activate
pip install -q bcrypt psycopg2-binary sqlalchemy asyncpg
check_status "Instalação de dependências"

log "🔑 Iniciando migração de senhas (Modo Produção)..."
# O script Python deve estar em apps/backend/tools/migration/ ou similar
python3 apps/backend/tools/migration/migrate_user_passwords.py --batch-size 100
check_status "Migração de senhas"

log "🚀 Reiniciando todos os serviços..."
docker compose up -d
check_status "Inicialização completa"

log "🔍 Validando Healthcheck..."
sleep 5
if curl -s -f http://localhost:8000/health > /dev/null; then
    success "Backend saudável após migração!"
else
    warn "Backend não respondeu ao healthcheck. Verifique 'docker compose logs backend'"
fi

success "Processo concluído. Backup em: $BACKUP_FILE"