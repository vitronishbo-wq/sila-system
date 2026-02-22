#!/bin/bash
# ===========================================
# Script para Iniciar Frontend em Desenvolvimento
# ===========================================

set -euo pipefail

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 Iniciando Frontend SILA System${NC}\n"

# Ir para diretório frontend
cd frontend

# Verificar se node_modules existe
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Instalando dependências...${NC}"
    npm install
fi

echo -e "${GREEN}✓ Dependências OK${NC}\n"

# Iniciar dev server
echo -e "${BLUE}🔥 Iniciando Vite dev server...${NC}\n"
cd apps/web
npm run dev -- --host 0.0.0.0 --port 5173
