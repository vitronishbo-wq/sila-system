#!/bin/bash

echo "╔════════════════════════════════════════════════════╗"
echo "║  🚀 SILA SYSTEM - AMBIENTE COMPLETO               ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_ROOT="/home/truman/dev/sila-system"
BACKEND_DIR="$PROJECT_ROOT/apps/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

echo -e "${BLUE}📍 Diretórios:${NC}"
echo "  Backend:  $BACKEND_DIR"
echo "  Frontend: $FRONTEND_DIR"
echo ""

# Função para iniciar backend
start_backend() {
    echo -e "${YELLOW}🔧 Iniciando Backend...${NC}"
    cd $BACKEND_DIR
    python3 main.py &
    BACKEND_PID=$!
    sleep 3
    echo -e "${GREEN}✅ Backend rodando (PID: $BACKEND_PID) em http://localhost:8000${NC}"
}

# Função para iniciar frontend
start_frontend() {
    echo -e "${YELLOW}🎨 Iniciando Frontend...${NC}"
    cd $FRONTEND_DIR
    npm run dev &
    FRONTEND_PID=$!
    sleep 3
    echo -e "${GREEN}✅ Frontend rodando (PID: $FRONTEND_PID) em http://localhost:5173${NC}"
}

# Função para iniciar ambos
start_all() {
    echo -e "${BLUE}Starting both services...${NC}"
    start_backend
    echo ""
    start_frontend

    echo ""
    echo -e "${GREEN}🎉 SILA SYSTEM rodando!${NC}"
    echo ""
    echo -e "Frontend:  ${BLUE}http://localhost:5173${NC}"
    echo -e "Backend:   ${BLUE}http://localhost:8000${NC}"
    echo -e "API Docs:  ${BLUE}http://localhost:8000/docs${NC}"
    echo ""
    echo "Pressione Ctrl+C para parar os servidores"

    wait
}

# Menu
case "$1" in
    backend)
        start_backend
        wait $BACKEND_PID
        ;;
    frontend)
        start_frontend
        wait $FRONTEND_PID
        ;;
    all|*)
        start_all
        ;;
esac
