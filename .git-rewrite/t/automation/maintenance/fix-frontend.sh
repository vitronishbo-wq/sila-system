#!/bin/bash

# ===========================================
# SILA Frontend Fix Script
# Automatiza correção de problemas do frontend
# ===========================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "\n${BLUE}========================================${NC}"; echo -e "${BLUE}🔧 $1${NC}"; echo -e "${BLUE}========================================${NC}"; }

# Navegar para raiz do projeto
cd "$(dirname "$0")/.." || exit 1
PROJECT_ROOT=$(pwd)

log_step "SILA Frontend Fix - Diagnóstico e Correção Automática"
log_info "Projeto: $PROJECT_ROOT"

# ===========================================
# 1. DIAGNÓSTICO
# ===========================================
log_step "1. Diagnóstico dos Problemas"

ISSUES_FOUND=0

# Verificar docker-compose.yml
if grep -q "context: ./frontend/apps/web" docker-compose.yml 2>/dev/null; then
    log_error "Context Docker errado encontrado"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    log_success "Context Docker correto"
fi

# Verificar client.ts
if grep -q "baseURL: 'http://localhost:8000" frontend/packages/shared-api/src/client.ts 2>/dev/null; then
    log_error "localhost hardcoded encontrado em client.ts"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    log_success "client.ts usando variáveis de ambiente"
fi

# Verificar .env.development
if [ ! -f "frontend/.env.development" ]; then
    log_error ".env.development ausente"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    log_success ".env.development presente"
fi

# Verificar Dockerfile
if ! grep -q "COPY package.json" frontend/apps/web/Dockerfile 2>/dev/null; then
    log_error "Dockerfile não suporta monorepo"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
else
    log_success "Dockerfile suporta monorepo"
fi

if [ $ISSUES_FOUND -eq 0 ]; then
    log_success "🎉 Nenhum problema encontrado! Frontend já está corrigido."
    exit 0
fi

log_warning "📊 $ISSUES_FOUND problema(s) encontrado(s). Aplicando correções..."

# ===========================================
# 2. BACKUP
# ===========================================
log_step "2. Criando Backup"

BACKUP_DIR=".backups/frontend-fix-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

[ -f "docker-compose.yml" ] && cp docker-compose.yml "$BACKUP_DIR/"
[ -f "frontend/packages/shared-api/src/client.ts" ] && cp frontend/packages/shared-api/src/client.ts "$BACKUP_DIR/"
[ -f "frontend/apps/web/Dockerfile" ] && cp frontend/apps/web/Dockerfile "$BACKUP_DIR/"

log_success "Backup criado em: $BACKUP_DIR"

# ===========================================
# 3. CORREÇÕES
# ===========================================
log_step "3. Aplicando Correções"

# Correção 1: docker-compose.yml
if grep -q "context: ./frontend/apps/web" docker-compose.yml; then
    log_info "Corrigindo context do Docker..."
    sed -i 's|context: ./frontend/apps/web|context: ./frontend|g' docker-compose.yml
    sed -i 's|dockerfile: Dockerfile|dockerfile: apps/web/Dockerfile|g' docker-compose.yml

    # Adicionar VITE_BACKEND_URL se não existir
    if ! grep -q "VITE_BACKEND_URL" docker-compose.yml; then
        sed -i '/container_name: sila-frontend/a\    environment:\n      - VITE_BACKEND_URL=http://sila-backend:8000' docker-compose.yml
    fi

    log_success "docker-compose.yml corrigido"
fi

# Correção 2: client.ts
if grep -q "baseURL: 'http://localhost:8000/api'" frontend/packages/shared-api/src/client.ts; then
    log_info "Corrigindo client.ts..."
    sed -i "s|baseURL: 'http://localhost:8000/api'|baseURL: \`\${import.meta.env.VITE_BACKEND_URL \|\| 'http://localhost:8000'}/api\`|g" frontend/packages/shared-api/src/client.ts
    log_success "client.ts corrigido"
else
    log_success "client.ts já está correto"
fi

# Correção 3: .env.development
if [ ! -f "frontend/.env.development" ]; then
    log_info "Criando .env.development..."
    cat > frontend/.env.development << 'EOF'
# ===========================================
# SILA Frontend - Development Environment
# ===========================================

# Backend API URL (for Docker containers)
VITE_BACKEND_URL=http://sila-backend:8000

# Development mode
NODE_ENV=development
VITE_NODE_ENV=development

# Debug mode
VITE_DEBUG=true

# API timeout
VITE_API_TIMEOUT=30000
EOF
    log_success ".env.development criado"
fi

# Correção 4: Dockerfile multi-stage
if ! grep -q "COPY package.json" frontend/apps/web/Dockerfile; then
    log_info "Corrigindo Dockerfile para monorepo..."
    cat > frontend/apps/web/Dockerfile << 'EOF'
# ===========================================
# Multi-stage build for SILA Frontend Monorepo
# ===========================================

# Stage 1: Build
FROM node:20-alpine AS builder

LABEL maintainer="SILA System <silahbo@gmail.com>"
LABEL description="SILA System Frontend - Build Stage"

WORKDIR /app

# Copy root package.json and workspace configuration
COPY package.json ./
COPY packages/ ./packages/
COPY apps/web/ ./apps/web/

# Install dependencies (npm workspaces)
RUN npm install

# Build the web app
RUN npm run build --workspace=@sila-system/web

# Stage 2: Production
FROM nginx:alpine

LABEL maintainer="SILA System <silahbo@gmail.com>"
LABEL description="SILA System Frontend - Production Server"
LABEL version="1.0.0"

RUN apk add --no-cache curl tzdata

ENV TZ=Africa/Luanda
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /usr/share/nginx/html

# Copy built assets from builder stage
COPY --from=builder /app/apps/web/dist/ /usr/share/nginx/html/

# Copy nginx configuration if exists
COPY apps/web/nginx.conf /etc/nginx/nginx.conf 2>/dev/null || echo "No custom nginx.conf found, using default"

RUN mkdir -p /var/log/nginx
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/log/nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
EOF
    log_success "Dockerfile corrigido para monorepo"
fi

# ===========================================
# 4. VALIDAÇÃO
# ===========================================
log_step "4. Validação das Correções"

# Validar docker-compose.yml
if docker compose config >/dev/null 2>&1; then
    log_success "docker-compose.yml válido"
else
    log_error "docker-compose.yml inválido"
    exit 1
fi

# Validar estrutura do frontend
if [ -d "frontend/apps/web" ] && [ -d "frontend/packages" ]; then
    log_success "Estrutura do monorepo válida"
else
    log_error "Estrutura do monorepo inválida"
    exit 1
fi

# ===========================================
# 5. TESTE OPCIONAL
# ===========================================
log_step "5. Teste (Opcional)"

read -p "🚀 Deseja testar o frontend agora? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "Iniciando teste do frontend..."

    # Verificar se Docker está rodando
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker não está rodando. Inicie o Docker Desktop primeiro."
        exit 1
    fi

    # Executar start_enterprise.sh
    log_info "Executando: ./start_enterprise.sh --frontend"
    ./start_enterprise.sh --frontend

    log_success "🎉 Teste concluído!"
    log_info "Acesse:"
    log_info "  🌐 Frontend: http://localhost"
    log_info "  🔙 Backend: http://localhost:8000"
    log_info "  📚 Docs: http://localhost:8000/docs"
else
    log_info "Teste pulado. Para testar manualmente:"
    log_info "  ./start_enterprise.sh --frontend"
fi

# ===========================================
# 6. RELATÓRIO FINAL
# ===========================================
log_step "6. Relatório Final"

log_success "🎉 Frontend Fix Concluído!"
log_info "📊 Correções aplicadas:"
log_info "  ✅ Context Docker: ./frontend"
log_info "  ✅ Dockerfile multi-stage para monorepo"
log_info "  ✅ API client com variáveis de ambiente"
log_info "  ✅ .env.development criado"
log_info ""
log_info "📁 Backup salvo em: $BACKUP_DIR"
log_info "🚀 Para testar: ./start_enterprise.sh --frontend"
log_info ""
log_success "✨ Frontend pronto para uso!"
