#!/bin/bash
# =============================================================================
# SILA: Seed Angola DPA 2024 - Script Completo
# =============================================================================
# Este script:
#   1. Configura DATABASE_URL para Alembic (formato psycopg2)
#   2. Roda as migrations
#   3. Executa o seed idempotente
#   4. Mostra os primeiros 50 registros da hierarquia
#
# Uso:
#   ./run_seed_angola.sh           # Roda tudo
#   ./run_seed_angola.sh --check   # Apenas verifica o estado atual
#   ./run_seed_angola.sh --show    # Apenas mostra hierarquia existente
# =============================================================================

set -e  # Para na primeira falha

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../.."
VENV_DIR="$BACKEND_DIR/../../venv"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}  SILA: Seed Angola DPA 2024${NC}"
echo -e "${BLUE}=============================================${NC}"
echo ""

# 1️⃣ Ativar virtualenv
echo -e "${YELLOW}📦 Ativando virtualenv...${NC}"
source "$VENV_DIR/bin/activate"

# 2️⃣ Carregar variáveis do .env
if [ -f "$BACKEND_DIR/.env" ]; then
    echo -e "${YELLOW}📄 Carregando .env...${NC}"
    export $(grep -v '^#' "$BACKEND_DIR/.env" | xargs)
fi

# 3️⃣ Configurar DATABASE_URL para Alembic (formato async)
# Alembic neste projeto usa create_async_engine, precisa de asyncpg
export DATABASE_URL="postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

echo -e "${GREEN}✅ DATABASE_URL configurado: postgresql+asyncpg://${DB_USER}:****@${DB_HOST}:${DB_PORT}/${DB_NAME}${NC}"
echo ""

cd "$BACKEND_DIR"

# Processar argumentos
if [ "$1" == "--check" ]; then
    echo -e "${BLUE}🔍 Modo --check: apenas verificando estado atual...${NC}"
    python seeds/core/seed_angola_dpa_v3.py --check
    exit 0
fi

if [ "$1" == "--show" ]; then
    echo -e "${BLUE}📋 Modo --show: mostrando hierarquia existente...${NC}"
    python seeds/core/seed_angola_dpa_v3.py --check
    python seeds/core/seed_angola_dpa_v3.py --show --limit 50
    exit 0
fi

# 4️⃣ Rodar migrations
echo -e "${YELLOW}🔧 Rodando Alembic migrations...${NC}"
alembic -c alembic_core/alembic.ini upgrade head
echo -e "${GREEN}✅ Migrations aplicadas com sucesso!${NC}"
echo ""

# 5️⃣ Rodar seed idempotente
echo -e "${YELLOW}🌍 Rodando seed Angola DPA 2024...${NC}"
python seeds/core/seed_angola_dpa_v3.py --show

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}  ✅ Seed completado com sucesso!${NC}"
echo -e "${GREEN}=============================================${NC}"
