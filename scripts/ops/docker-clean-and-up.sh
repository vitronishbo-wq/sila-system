#!/bin/bash
set -e

echo "🧹 LIMPEZA AUTOMÁTICA E INICIALIZAÇÃO DO DOCKER"
echo "=================================================="
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Parar containers antigos
echo -e "${YELLOW}[1/5]${NC} Parando containers antigos..."
docker ps -a --format '{{.Names}}' | grep -E 'sila-|postgres|redis' | xargs -r docker stop 2>/dev/null || true
echo -e "${GREEN}✅ Containers parados${NC}"

# 2. Remover containers
echo -e "${YELLOW}[2/5]${NC} Removendo containers..."
docker ps -a --format '{{.Names}}' | grep -E 'sila-|postgres|redis' | xargs -r docker rm -f 2>/dev/null || true
echo -e "${GREEN}✅ Containers removidos${NC}"

# 3. Liberar portas (matar processos)
echo -e "${YELLOW}[3/5]${NC} Liberando portas (80, 443, 8000, 5432, 6379)..."
for PORT in 80 443 8000 5432 6379; do
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "  Matando processo na porta $PORT..."
        lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    fi
done
echo -e "${GREEN}✅ Portas liberadas${NC}"

# 4. Limpar volumes órfãos
echo -e "${YELLOW}[4/5]${NC} Limpando sistema Docker..."
docker system prune -f --volumes 2>/dev/null || true
echo -e "${GREEN}✅ Sistema limpo${NC}"

# 5. Iniciar docker-compose
echo -e "${YELLOW}[5/5]${NC} Iniciando containers..."
docker compose up -d

echo ""
echo -e "${GREEN}=================================================="
echo "✅ DOCKER INICIADO COM SUCESSO!"
echo "=================================================="
echo ""
echo "📋 Verificação:"
docker compose ps
echo ""
echo "🌐 Acesso:"
echo "  Frontend: http://localhost"
echo "  Backend:  http://localhost:8000"
echo "  Database: localhost:5432"
echo "  Redis:    localhost:6379"
