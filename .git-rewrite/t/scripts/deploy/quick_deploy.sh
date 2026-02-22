#!/bin/bash

# =================================================================
# QUICK DEPLOY - Deploy rápido sem perguntas
# Versão simplificada do deploy_final.sh para uso diário
# Otimizado para HD interno (/mnt/sda2)
# =================================================================

# Diretório base (detectado automaticamente a partir da localização do script
# ou da raiz do repositório git).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if git -C "$SCRIPT_DIR" rev-parse --show-toplevel >/dev/null 2>&1; then
    BASE_DIR="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
else
    BASE_DIR="$SCRIPT_DIR"
fi

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}🚀 Quick Deploy - Sila System${NC}"
echo ""

# Garante execução a partir da raiz do repositório
cd "$BASE_DIR"

# Check if there are changes
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${GREEN}✅ Nenhuma alteração detectada. Sistema já está atualizado.${NC}"
    exit 0
fi

# Run full deploy via Makefile / Docker Compose unificado
echo "Executando deploy completo via Makefile (make up-dev)..."
make up-dev

exit $?
