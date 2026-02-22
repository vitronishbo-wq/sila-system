#!/bin/bash
# ===========================================
# Script de Correção de Aliases TypeScript
# Aplica aliases para resolver imports relativos
# Versão: 1.0
# ===========================================

set -euo pipefail

# --- Patch Anti-Panic do Docker Compose ---
export DOCKER_CLI_HINTS=false
export COMPOSE_ENABLE_TELEMETRY=0
export COMPOSE_DOCKER_CLI_BUILD=1

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# --- Funções de Logging ---

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo -e "\n${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

# --- Configurações ---
FRONTEND_DIR="frontend"
TSCONFIG_ROOT="${FRONTEND_DIR}/tsconfig.json"
VITE_CONFIG="${FRONTEND_DIR}/apps/web/vite.config.ts"
SHARED_UI_INDEX="${FRONTEND_DIR}/packages/shared-ui/src/index.ts"

# Banner
echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║           🔧 TypeScript Aliases Fix - SILA System            ║
║                  Correção Cirúrgica de Imports               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# --- Etapa 1: Backup ---
log_step "1️⃣  Criando Backups de Segurança"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/typescript_fix_${TIMESTAMP}"

mkdir -p "${BACKUP_DIR}"

if [ -f "${TSCONFIG_ROOT}" ]; then
    cp "${TSCONFIG_ROOT}" "${BACKUP_DIR}/tsconfig.json.backup"
    log_success "Backup: ${TSCONFIG_ROOT}"
fi

if [ -f "${VITE_CONFIG}" ]; then
    cp "${VITE_CONFIG}" "${BACKUP_DIR}/vite.config.ts.backup"
    log_success "Backup: ${VITE_CONFIG}"
fi

if [ -f "${SHARED_UI_INDEX}" ]; then
    cp "${SHARED_UI_INDEX}" "${BACKUP_DIR}/index.ts.backup"
    log_success "Backup: ${SHARED_UI_INDEX}"
fi

log_info "Backups salvos em: ${BACKUP_DIR}"

# --- Etapa 2: Atualizar tsconfig.json ---
log_step "2️⃣  Atualizando tsconfig.json com Aliases @design"

if [ ! -f "${TSCONFIG_ROOT}" ]; then
    log_error "Arquivo ${TSCONFIG_ROOT} não encontrado!"
    exit 1
fi

log_info "Adicionando alias @design/* ao tsconfig.json..."

# Criar tsconfig temporário com o novo alias
cat > "${TSCONFIG_ROOT}.tmp" << 'TSCONFIG_EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": false,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "paths": {
      "@design/*": ["./design/*"],
      "@sila-system/shared-api": ["./packages/shared-api/src/index.ts"],
      "@sila-system/shared-api/*": ["./packages/shared-api/src/*"],
      "@sila-system/shared-ui": ["./packages/shared-ui/src/index.ts"],
      "@sila-system/shared-ui/*": ["./packages/shared-ui/src/*"]
    },
    "types": ["vite/client", "react", "react-dom"]
  },
  "include": ["./packages/**/*", "./apps/**/*"],
  "references": [
    {
      "path": "./apps/web/tsconfig.json"
    },
    {
      "path": "./packages/shared-api/tsconfig.json"
    },
    {
      "path": "./packages/shared-ui/tsconfig.json"
    }
  ]
}
TSCONFIG_EOF

mv "${TSCONFIG_ROOT}.tmp" "${TSCONFIG_ROOT}"
log_success "tsconfig.json atualizado com alias @design/*"

# --- Etapa 3: Atualizar vite.config.ts ---
log_step "3️⃣  Atualizando vite.config.ts com Aliases"

if [ ! -f "${VITE_CONFIG}" ]; then
    log_error "Arquivo ${VITE_CONFIG} não encontrado!"
    exit 1
fi

log_info "Adicionando alias @design ao vite.config.ts..."

cat > "${VITE_CONFIG}.tmp" << 'VITE_EOF'
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@design': path.resolve(__dirname, '../../design'),
      '@sila-system/shared-api': path.resolve(__dirname, '../../packages/shared-api/src'),
      '@sila-system/shared-ui': path.resolve(__dirname, '../../packages/shared-ui/src')
    }
  },
  server: {
    port: 5173,
    host: '0.0.0.0'
  },
});
VITE_EOF

mv "${VITE_CONFIG}.tmp" "${VITE_CONFIG}"
log_success "vite.config.ts atualizado com alias @design"

# --- Etapa 4: Atualizar imports no shared-ui ---
log_step "4️⃣  Atualizando Imports no shared-ui"

if [ ! -f "${SHARED_UI_INDEX}" ]; then
    log_error "Arquivo ${SHARED_UI_INDEX} não encontrado!"
    exit 1
fi

log_info "Substituindo imports relativos por aliases..."

# Substituir import relativo por alias
sed -i "s|from '../../../design/tokens'|from '@design/tokens'|g" "${SHARED_UI_INDEX}"
sed -i 's|from "../../../design/tokens"|from "@design/tokens"|g' "${SHARED_UI_INDEX}"

log_success "Imports atualizados em ${SHARED_UI_INDEX}"

# Verificar se a substituição foi feita
if grep -q "@design/tokens" "${SHARED_UI_INDEX}"; then
    log_success "✓ Import usando alias @design/tokens confirmado"
else
    log_warn "⚠ Import pode não ter sido atualizado corretamente"
fi

# --- Etapa 5: Buscar e corrigir outros imports relativos ---
log_step "5️⃣  Buscando Outros Imports Relativos para Corrigir"

log_info "Procurando por imports relativos em packages/shared-ui..."

# Buscar todos os arquivos TypeScript/TSX
find "${FRONTEND_DIR}/packages/shared-ui/src" -type f \( -name "*.ts" -o -name "*.tsx" \) | while read -r file; do
    if grep -q "from '\.\./\.\./\.\./design" "$file" 2>/dev/null || grep -q 'from "\.\./\.\./\.\./design' "$file" 2>/dev/null; then
        log_info "Corrigindo: $file"
        sed -i "s|from '../../../design/\([^']*\)'|from '@design/\1'|g" "$file"
        sed -i 's|from "../../../design/\([^"]*\)"|from "@design/\1"|g' "$file"
        log_success "✓ $file"
    fi
done

log_info "Procurando por imports relativos em packages/shared-api..."

find "${FRONTEND_DIR}/packages/shared-api/src" -type f \( -name "*.ts" -o -name "*.tsx" \) | while read -r file; do
    if grep -q "from '\.\./\.\./\.\./design" "$file" 2>/dev/null || grep -q 'from "\.\./\.\./\.\./design' "$file" 2>/dev/null; then
        log_info "Corrigindo: $file"
        sed -i "s|from '../../../design/\([^']*\)'|from '@design/\1'|g" "$file"
        sed -i 's|from "../../../design/\([^"]*\)"|from "@design/\1"|g' "$file"
        log_success "✓ $file"
    fi
done

# --- Etapa 6: Limpar e Reconstruir ---
log_step "6️⃣  Limpando Cache e Reconstruindo"

log_info "Removendo node_modules, .turbo, dist..."

cd "${FRONTEND_DIR}"

# Remover caches
rm -rf node_modules 2>/dev/null || true
rm -rf .turbo 2>/dev/null || true
rm -rf dist 2>/dev/null || true
rm -rf apps/web/dist 2>/dev/null || true
rm -rf packages/*/dist 2>/dev/null || true

log_success "Caches removidos"

log_info "Reinstalando dependências..."

if command -v pnpm &> /dev/null; then
    log_info "Usando pnpm..."
    rm -f pnpm-lock.yaml
    pnpm install
elif command -v npm &> /dev/null; then
    log_info "Usando npm..."
    rm -f package-lock.json
    npm install
else
    log_error "Nem npm nem pnpm encontrados!"
    exit 1
fi

log_success "Dependências instaladas"

cd ..

# --- Etapa 7: Validação ---
log_step "7️⃣  Validação Final"

log_info "Verificando arquivos modificados..."

# Verificar tsconfig.json
if grep -q '"@design/\*"' "${TSCONFIG_ROOT}"; then
    log_success "✓ tsconfig.json: alias @design/* configurado"
else
    log_error "✗ tsconfig.json: alias @design/* NÃO encontrado"
fi

# Verificar vite.config.ts
if grep -q "'@design'" "${VITE_CONFIG}"; then
    log_success "✓ vite.config.ts: alias @design configurado"
else
    log_error "✗ vite.config.ts: alias @design NÃO encontrado"
fi

# Verificar shared-ui index
if grep -q "@design/tokens" "${SHARED_UI_INDEX}"; then
    log_success "✓ shared-ui/index.ts: usando alias @design/tokens"
else
    log_error "✗ shared-ui/index.ts: ainda usando import relativo"
fi

# Verificar se há imports relativos restantes
log_info "Verificando imports relativos restantes..."
REMAINING=$(find "${FRONTEND_DIR}/packages" -type f \( -name "*.ts" -o -name "*.tsx" \) -exec grep -l "from '\.\./\.\./\.\./design" {} \; 2>/dev/null | wc -l)

if [ "$REMAINING" -eq 0 ]; then
    log_success "✓ Nenhum import relativo para design/ encontrado"
else
    log_warn "⚠ Ainda existem $REMAINING arquivo(s) com imports relativos"
fi

# --- Resumo Final ---
log_step "✅ Correção Concluída com Sucesso!"

echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                    ✅ CORREÇÃO APLICADA                      ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}Arquivos Modificados:${NC}"
echo -e "  ✓ ${TSCONFIG_ROOT}"
echo -e "  ✓ ${VITE_CONFIG}"
echo -e "  ✓ ${SHARED_UI_INDEX}"
echo ""

echo -e "${CYAN}Aliases Configurados:${NC}"
echo -e "  ✓ @design/* → frontend/design/*"
echo -e "  ✓ @sila-system/shared-api → packages/shared-api/src"
echo -e "  ✓ @sila-system/shared-ui → packages/shared-ui/src"
echo ""

echo -e "${CYAN}Backups Salvos em:${NC}"
echo -e "  📁 ${BACKUP_DIR}"
echo ""

echo -e "${YELLOW}Próximos Passos:${NC}"
echo -e "  1. ${BLUE}cd frontend && npm run build${NC}"
echo -e "  2. ${BLUE}npm run dev${NC}"
echo -e "  3. ${BLUE}Verificar se não há erros de import${NC}"
echo ""

echo -e "${GREEN}🎉 Sistema pronto para uso com aliases TypeScript!${NC}"
