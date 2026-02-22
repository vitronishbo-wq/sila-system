#!/bin/bash

echo "🔧 INICIANDO SANEAMENTO DE DEPENDÊNCIAS FRONTEND SILA"
echo "📍 Diretório base: /opt/sila-system/frontend"

# ETAPA 1: Atualizar TypeScript no shared-ui
echo "📦 Atualizando TypeScript no shared-ui..."
cd /opt/sila-system/frontend/packages/shared-ui
npm install --save-dev typescript@5.2.2

# ETAPA 2: Atualizar React, TypeScript e Axios no shared-api
echo "📦 Atualizando React, TypeScript e Axios no shared-api..."
cd /opt/sila-system/frontend/packages/shared-api
npm install react@18.3.1 react-dom@18.3.1
npm install --save-dev typescript@5.2.2
npm install axios@1.12.2

# ETAPA 3: Atualizar React, Zustand e TypeScript no apps/web
echo "📦 Atualizando React, Zustand e TypeScript no apps/web..."
cd /opt/sila-system/frontend/apps/web
npm install react@18.3.1 react-dom@18.3.1
npm install zustand@4.5.7
npm install --save-dev typescript@5.2.2

# ETAPA 4: Atualizar Vite e dependências vulneráveis na raiz
echo "🔐 Atualizando Vite, Vitest e Vite-node na raiz..."
cd /opt/sila-system/frontend
npm install vite@latest vitest@latest vite-node@latest

# ETAPA 5: Atualizar Vite também dentro de apps/web
echo "🔐 Atualizando Vite, Vitest e Vite-node no apps/web..."
cd /opt/sila-system/frontend/apps/web
npm install vite@latest vitest@latest vite-node@latest

# ETAPA 6: Validar build final
echo "🧪 Validando build final..."
cd /opt/sila-system/frontend
npm run build --workspace=@sila-system/web

echo "✅ SANEAMENTO COMPLETO!"
