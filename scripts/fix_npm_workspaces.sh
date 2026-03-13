#!/usr/bin/env bash
set -euo pipefail

# Configurações de Cores para Terminal
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${YELLOW}🔧 SILA NPM WORKSPACES: SOVEREIGN REPAIR${NC}"
echo -e "${BLUE}========================================${NC}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# 1. Validação de Nomes e Identidade
echo -e "\n${YELLOW}[1/5] Validando Identidades de Pacotes...${NC}"

# Extração de nomes usando node (mais robusto que sed/grep)
get_name() {
    node -e "console.log(require('./$1/package.json').name)" 2>/dev/null || echo "not_found"
}

ROOT_NAME=$(get_name ".")
APPS_NAME=$(get_name "apps/frontend")
INTERFACE_NAME=$(get_name "interfaces/frontend")

echo -e "  📍 Root: ${BLUE}$ROOT_NAME${NC}"
echo -e "  📍 Apps: ${BLUE}$APPS_NAME${NC}"
echo -e "  📍 Interface: ${BLUE}$INTERFACE_NAME${NC}"

if [ "$APPS_NAME" == "$INTERFACE_NAME" ] && [ "$APPS_NAME" != "not_found" ]; then
    echo -e "${RED}❌ ERRO: Colisão de nomes detectada! Ambas as pastas usam '$APPS_NAME'.${NC}"
    echo -e "${YELLOW}Dica: Altere o 'name' em apps/frontend/package.json para 'sila-frontend-app'.${NC}"
    exit 1
fi

# 2. Verificação de Configuração de Workspace
echo -e "\n${YELLOW}[2/5] Verificando Constituição do Workspace...${NC}"
if ! grep -q "\"workspaces\"" package.json; then
    echo -e "${RED}⚠️  AVISO: 'workspaces' não configurado no package.json da raiz.${NC}"
    echo -e "Adicionando configuração padrão..."
    # Adiciona workspaces se não existir (usa python para edição segura de JSON)
    python3 -c "import json; d=json.load(open('package.json')); d['workspaces']=['apps/*','interfaces/*']; json.dump(d, open('package.json','w'), indent=2)"
fi
echo -e "${GREEN}✓ Workspaces configurados.${NC}"

# 3. Limpeza Atômica
echo -e "\n${YELLOW}[3/5] Executando Limpeza Atômica de Caches...${NC}"
# Remove apenas o que é lixo, protegendo arquivos de sistema (como o erro wsl.localhost)
rm -rf node_modules package-lock.json
find . -mindepth 2 -name "node_modules" -type d -not -path "./.git/*" -exec rm -rf {} +
find . -name "package-lock.json" -not -path "./package-lock.json" -delete

echo -e "${GREEN}✓ Caches e links simbólicos removidos.${NC}"

# 4. Reconstrução do Ecossistema
echo -e "\n${YELLOW}[4/5] Reinstalando Dependências (Modo Clean)...${NC}"
npm install --prefer-offline --no-audit --loglevel=error

# 5. Auditoria de Integridade
echo -e "\n${YELLOW}[5/5] Auditoria Final de Estrutura...${NC}"
if npm ls --depth=0 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ ESTRUTURA VÁLIDA: Workspaces vinculados corretamente.${NC}"
else
    echo -e "${RED}❌ FALHA: NPM detectou inconsistências após a instalação.${NC}"
    exit 1
fi

echo -e "\n${GREEN}🚀 REPARAÇÃO CONCLUÍDA COM SUCESSO!${NC}"
echo -e "${BLUE}========================================${NC}"
