#!/bin/bash
# ===========================================
# scripts/seed.sh
# Executa seed do dashboard em 30 segundos
# ===========================================

set -e

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║  🌱 SEED DASHBOARD - SILA SYSTEM           ║"
echo "║  Populando com dados reais (Angola 2025)   ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar se estamos no diretório correto
if [ ! -f "main.py" ]; then
    echo -e "${YELLOW}⚠️  Navegando para apps/backend...${NC}"
    cd apps/backend 2>/dev/null || {
        echo "❌ Erro: não conseguiu encontrar apps/backend"
        exit 1
    }
fi

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    exit 1
fi

echo -e "${BLUE}✓ Ambiente verificado${NC}"
echo ""

# Executar seed
echo -e "${BLUE}→ Executando seed...${NC}"
python3 scripts/seed_dashboard.py

echo ""
echo -e "${GREEN}✅ Dashboard pronto com dados reais!${NC}"
echo ""
echo "📍 Próximo passo:"
echo "   1. Acesse: http://localhost:5173"
echo "   2. Faça login: admin@sila.gov.ao / adm123"
echo "   3. Veja as métricas carregadas! 🎉"
echo ""
