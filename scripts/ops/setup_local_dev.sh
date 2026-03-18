#!/bin/bash
set -e

# ==============================
# 🚀 SETUP LOCAL - SILA SYSTEM
# ==============================
# Automatiza setup de desenvolvimento sem Docker
# Data: 2026-02-23
# Execução: bash setup_local_dev.sh

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Variáveis
POSTGRES_USER="sila_user"
POSTGRES_PASSWORD="Trumanmarcelo_1983"
POSTGRES_DB="sila_db"
VENV_PATH="apps/backend/.venv"
PYTHON_CMD="python3"

# Funções helpers
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# ==============================
# STEP 1: Verificar ferramentas
# ==============================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PASSO 1: Verificando ferramentas${NC}"
echo -e "${BLUE}========================================${NC}"

log_info "Verificando Python 3.12+..."
if ! command -v $PYTHON_CMD &> /dev/null; then
    log_error "Python3 não encontrado"
    exit 1
fi
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
log_success "Python $PYTHON_VERSION encontrado"

log_info "Verificando PostgreSQL..."
if ! command -v psql &> /dev/null; then
    log_error "psql não encontrado. Instalar: sudo apt install -y postgresql"
    exit 1
fi
PG_VERSION=$(psql --version 2>&1 | awk '{print $NF}')
log_success "PostgreSQL $PG_VERSION encontrado"

log_info "Verificando Redis..."
if ! command -v redis-cli &> /dev/null; then
    log_error "redis-cli não encontrado. Instalar: sudo apt install -y redis-server"
    exit 1
fi
log_success "Redis encontrado"

log_info "Verificando sudo..."
if ! sudo -n true 2>/dev/null; then
    log_warn "Será necessário fornecer senha sudo"
fi
log_success "Todas as ferramentas presentes"

# ==============================
# STEP 2: Iniciar serviços
# ==============================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PASSO 2: Iniciando serviços PostgreSQL e Redis${NC}"
echo -e "${BLUE}========================================${NC}"

log_info "Iniciando PostgreSQL..."
sudo systemctl start postgresql
sleep 2
if sudo systemctl is-active --quiet postgresql; then
    log_success "PostgreSQL rodando"
else
    log_error "PostgreSQL falhou ao iniciar"
    exit 1
fi

log_info "Iniciando Redis..."
sudo systemctl start redis-server
sleep 1
if sudo systemctl is-active --quiet redis-server; then
    log_success "Redis rodando"
else
    log_error "Redis falhou ao iniciar"
    exit 1
fi

# ==============================
# STEP 3: Criar user PostgreSQL
# ==============================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PASSO 3: Configurando PostgreSQL${NC}"
echo -e "${BLUE}========================================${NC}"

log_info "Verificando user '$POSTGRES_USER'..."
USER_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'" 2>/dev/null || echo "0")

if [ "$USER_EXISTS" = "1" ]; then
    log_success "User '$POSTGRES_USER' já existe"
else
    log_info "Criando user '$POSTGRES_USER'..."
    sudo -u postgres psql -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD' CREATEDB;" 2>/dev/null || log_warn "User pode já existir"
    log_success "User criado/confirmado"
fi

# ==============================
# STEP 4: Criar DB
# ==============================
log_info "Verificando database '$POSTGRES_DB'..."
DB_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'" 2>/dev/null || echo "0")

if [ "$DB_EXISTS" = "1" ]; then
    log_success "Database '$POSTGRES_DB' já existe"
else
    log_info "Criando database '$POSTGRES_DB'..."
    sudo -u postgres createdb -O $POSTGRES_USER $POSTGRES_DB 2>/dev/null || log_warn "Database pode já existir"
    log_success "Database criado/confirmado"
fi

# ==============================
# STEP 5: Testar conexão
# ==============================
log_info "Testando conexão PostgreSQL..."
if PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1;" &>/dev/null; then
    log_success "Conexão PostgreSQL OK"
else
    log_error "Falha ao conectar ao PostgreSQL"
    exit 1
fi

# ==============================
# STEP 6: Testar Redis
# ==============================
log_info "Testando conexão Redis..."
if redis-cli ping 2>/dev/null | grep -q "PONG"; then
    log_success "Conexão Redis OK"
else
    log_error "Falha ao conectar ao Redis"
    exit 1
fi

# ==============================
# STEP 7: Copiar .env.local
# ==============================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PASSO 7: Configurando ambiente${NC}"
echo -e "${BLUE}========================================${NC}"

if [ -f ".env.local" ]; then
    log_info "Copiando .env.local para apps/backend/.env..."
    cp .env.local apps/backend/.env
    log_success ".env criado em apps/backend/"
else
    log_error ".env.local não encontrado em $(pwd)"
    exit 1
fi

# ==============================
# STEP 8: Setup Python venv
# ==============================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PASSO 8: Setup Python Virtual Environment${NC}"
echo -e "${BLUE}========================================${NC}"

if [ -d "$VENV_PATH" ]; then
    log_success "venv já existe em $VENV_PATH"
else
    log_info "Criando venv em $VENV_PATH..."
    cd apps/backend
    $PYTHON_CMD -m venv .venv
    log_success "venv criado"
    cd - > /dev/null
fi

log_info "Ativando venv e instalando dependências..."
source "$VENV_PATH/bin/activate"

log_info "Upgrade pip..."
pip install --upgrade pip setuptools wheel -q
log_success "pip atualizado"

log_info "Instalando dependências (dev.txt)..."
pip install -r apps/backend/requirements/dev.txt -q
log_success "Dependências instaladas"

# ==============================
# STEP 9: Migrations (Alembic)
# ==============================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}PASSO 9: Executando Migrações${NC}"
echo -e "${BLUE}========================================${NC}"

cd apps/backend

log_info "Verificando status de migrações..."
CURRENT_MIGRATION=$(alembic current 2>/dev/null || echo "Nenhuma")
log_info "Migração atual: $CURRENT_MIGRATION"

log_info "Executando alembic upgrade head..."
alembic upgrade head
log_success "Migrações aplicadas"

cd - > /dev/null

# ==============================
# STEP 10: Resumo
# ==============================
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ SETUP COMPLETO!${NC}"
echo -e "${BLUE}========================================${NC}"

echo ""
echo -e "${YELLOW}📋 PRÓXIMOS PASSOS:${NC}"
echo ""
echo "1️⃣  Ativar venv (em novo terminal):"
echo -e "   ${BLUE}cd /home/dev03wsl/sila-system${NC}"
echo -e "   ${BLUE}source apps/backend/.venv/bin/activate${NC}"
echo ""
echo "2️⃣  (Opcional) Carregar seeds no DB:"
echo -e "   ${BLUE}python scripts/seeds/core/seed_and_token.py${NC}"
echo ""
echo "3️⃣  Iniciar Backend:"
echo -e "   ${BLUE}cd apps/backend${NC}"
echo -e "   ${BLUE}uvicorn main:app --host localhost --port 8000 --reload${NC}"
echo ""
echo "4️⃣  Testar API (novo terminal):"
echo -e "   ${BLUE}curl -s http://localhost:8000/api/v1/health | jq .${NC}"
echo ""
echo -e "${YELLOW}🔍 VERIFICAÇÕES RÁPIDAS:${NC}"
echo ""
echo "PostgreSQL:"
echo -e "   ${BLUE}PGPASSWORD=\"$POSTGRES_PASSWORD\" psql -h localhost -U $POSTGRES_USER -d $POSTGRES_DB -c \"\\\\dt\"${NC}"
echo ""
echo "Redis:"
echo -e "   ${BLUE}redis-cli ping${NC}"
echo ""
echo "Backend Health:"
echo -e "   ${BLUE}curl http://localhost:8000/api/v1/health${NC}"
echo ""
