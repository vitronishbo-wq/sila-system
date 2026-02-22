#!/bin/bash

# SILA Frontend - Generator Script
# Cria estrutura completa do frontend com todas as dependências

set -e

PROJECT_ROOT="/home/truman/dev/sila-system"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "$BLUE╔══════════════════════════════════════════════════════════╗$NC"
echo -e "$BLUE║  🎨 SILA FRONTEND - GENERATOR$NC"
echo -e "$BLUE╚══════════════════════════════════════════════════════════╝$NC"
echo ""

# 1. Limpar instalação anterior
echo -e "$YELLOW[1/6]$NC Limpando instalação anterior..."
cd "$FRONTEND_DIR"
rm -rf node_modules package-lock.json 2>/dev/null || true
echo -e "$GREEN✓$NC node_modules e package-lock removidos"

# 2. Atualizar package.json com versões estáveis
echo -e "$YELLOW[2/6]$NC Atualizando package.json..."
cat > "$FRONTEND_DIR/package.json" << 'PKGJSON'
{
  "name": "sila-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "@tanstack/react-query": "^5.25.0",
    "@heroicons/react": "^2.0.18"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@types/node": "^20.10.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.3",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.6",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0"
  }
}
PKGJSON
echo -e "$GREEN✓$NC package.json atualizado com versões estáveis"

# 3. Configurar npm registry
echo -e "$YELLOW[3/6]$NC Configurando npm..."
npm config set registry https://registry.npmjs.org/
npm config set fetch-timeout=120000
npm config set fetch-retry-mintimeout=10000
npm config set fetch-retry-maxtimeout=120000
echo -e "$GREEN✓$NC npm configurado"

# 4. Instalar dependências
echo -e "$YELLOW[4/6]$NC Instalando dependências npm..."
npm install --legacy-peer-deps 2>&1 | grep -E "added|up to date|ERR" | tail -3 || true
if [ -d "node_modules" ]; then
    echo -e "$GREEN✓$NC npm dependencies instaladas"
else
    echo -e "$RED✗$NC Erro na instalação npm"
    exit 1
fi

# 5. Criar arquivos de configuração
echo -e "$YELLOW[5/6]$NC Criando arquivos de configuração..."

# vite.config.ts
cat > "$FRONTEND_DIR/vite.config.ts" << 'VITECFG'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    strictPort: false,
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})
VITECFG

# tsconfig.json
cat > "$FRONTEND_DIR/tsconfig.json" << 'TSCFG'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
TSCFG

# tsconfig.node.json
cat > "$FRONTEND_DIR/tsconfig.node.json" << 'TSNODECFG'
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
TSNODECFG

# tailwind.config.js
cat > "$FRONTEND_DIR/tailwind.config.js" << 'TAILWINDCFG'
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
TAILWINDCFG

# postcss.config.js
cat > "$FRONTEND_DIR/postcss.config.js" << 'POSTCSSCFG'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
POSTCSSCFG

echo -e "$GREEN✓$NC Configurações criadas"

# 6. Status final
echo -e "$YELLOW[6/6]$NC Verificando instalação..."
if command -v node >/dev/null && [ -d "node_modules/vite" ]; then
    echo ""
    echo -e "$GREEN╔══════════════════════════════════════════════════════════╗$NC"
    echo -e "$GREEN║  ✅ FRONTEND PRONTO PARA USAR$NC"
    echo -e "$GREEN╚══════════════════════════════════════════════════════════╝$NC"
    echo ""
    echo -e "Para iniciar o desenvolvimento:"
    echo -e "  $BLUE cd $FRONTEND_DIR$NC"
    echo -e "  $BLUE npm run dev$NC"
    echo ""
else
    echo -e "$RED✗ Erro na geração$NC"
    exit 1
fi
