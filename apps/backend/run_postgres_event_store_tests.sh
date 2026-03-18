#!/bin/bash

# Script para rodar testes do PostgreSQL EventStore
# Esta script espera pelo PostgreSQL e executa os testes

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}PostgreSQL EventStore Integration Tests${NC}"
echo "=========================================="

# Verificar se estamos no diretório correto
if [ ! -f "pytest.ini" ]; then
    echo -e "${RED}Error: pytest.ini not found. Please run from apps/backend directory${NC}"
    exit 1
fi

# Ativar virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${RED}Error: .venv directory not found. Please create virtual environment first${NC}"
    exit 1
fi

source .venv/bin/activate

# Exportar variáveis de ambiente necessárias
export PYTHONPATH=.
export ENVIRONMENT=test

# Tentar obter DATABASE_URL do .env se não estiver já configurado
if [ -z "$DATABASE_URL" ]; then
    if [ -f ".env" ]; then
        export DATABASE_URL=$(grep "^DATABASE_URL=" .env | cut -d'=' -f2)
    else
        # Usar padrão local
        export DATABASE_URL="postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    fi
fi

echo -e "${YELLOW}Using DATABASE_URL: $DATABASE_URL${NC}"

# Aguardar PostgreSQL estar pronto (máximo 60 segundos)
echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if python -c "import asyncio; from sqlalchemy.ext.asyncio import create_async_engine; asyncio.run(create_async_engine('$DATABASE_URL').connect())" 2>/dev/null; then
        echo -e "${GREEN}PostgreSQL is ready!${NC}"
        break
    fi
    echo -n "."
    sleep 2
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}PostgreSQL not available after $((MAX_RETRIES * 2)) seconds${NC}"
    echo -e "${YELLOW}Skipping database tests, running in-memory tests only${NC}"
    # Continuar anyway para testar lógica em memória
fi

echo ""

# Rodar testes do PostgreSQL EventStore
echo -e "${YELLOW}Running PostgreSQL EventStore Tests...${NC}"
python -m pytest tests/integration/test_postgres_event_store.py -v --tb=short --asyncio-mode=auto

# Verificar resultado
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}PostgreSQL EventStore tests completed successfully!${NC}"
