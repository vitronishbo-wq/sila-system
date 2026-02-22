#!/bin/bash
# ===========================================
# Script Simplificado para Desenvolvimento
# Inicia apenas backend e DB, frontend manualmente
# ===========================================

set -euo pipefail

# --- Patch Anti-Panic do Docker Compose ---
export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export COMPOSE_DOCKER_CLI_BUILD=1

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Iniciando SILA System (Modo Desenvolvimento Simplificado)${NC}\n"

# Parar containers antigos
echo -e "${YELLOW}Parando containers antigos...${NC}"
docker compose down 2>/dev/null || true

# Iniciar apenas backend e DB
echo -e "${BLUE}Iniciando Backend e PostgreSQL...${NC}"
docker compose up -d db backend

echo -e "${GREEN}✓ Backend e DB iniciados${NC}\n"

# Aguardar backend
echo -e "${YELLOW}Aguardando backend ficar pronto...${NC}"
sleep 10

# Verificar status
echo -e "${BLUE}Status dos containers:${NC}"
docker compose ps

echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Backend rodando!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${BLUE}URLs:${NC}"
echo -e "  Backend API: ${GREEN}http://localhost:8000${NC}"
echo -e "  API Docs:    ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  Healthcheck: ${GREEN}http://localhost:9111/health${NC}\n"

echo -e "${YELLOW}Para iniciar o frontend manualmente:${NC}"
echo -e "  ${BLUE}cd frontend${NC}"
echo -e "  ${BLUE}npm run dev${NC}\n"

echo -e "${YELLOW}Ou execute:${NC}"
echo -e "  ${BLUE}./scripts/start_frontend_dev.sh${NC}\n"
