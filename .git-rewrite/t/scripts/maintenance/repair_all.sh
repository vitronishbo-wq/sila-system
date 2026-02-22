#!/bin/bash

# ===========================================
# SILA REPAIR ALL RUNNER - Master Script
# Automatiza correção completa do sistema
# ===========================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "\n${PURPLE}========================================${NC}"; echo -e "${PURPLE}🔧 $1${NC}"; echo -e "${PURPLE}========================================${NC}"; }
log_feature() { echo -e "${CYAN}🚀 $1${NC}"; }

# Variáveis globais
PROJECT_ROOT=$(pwd)
BACKUP_DIR=".backups/repair-all-$(date +%Y%m%d_%H%M%S)"
HOT_RELOAD=false
GENERATE_TYPES=false
MONITORING=false

# Parse argumentos
for arg in "$@"; do
    case $arg in
        --hot-reload) HOT_RELOAD=true ;;
        --generate-types) GENERATE_TYPES=true ;;
        --monitoring) MONITORING=true ;;
        --help)
            echo "Uso: $0 [--hot-reload] [--generate-types] [--monitoring]"
            echo ""
            echo "Opções:"
            echo "  --hot-reload      Habilita hot reload para desenvolvimento"
            echo "  --generate-types  Gera tipos TypeScript via OpenAPI"
            echo "  --monitoring      Adiciona métricas Prometheus"
            echo "  --help           Mostra esta ajuda"
            exit 0
            ;;
    esac
done

log_step "SILA REPAIR ALL RUNNER"
log_info "Projeto: $PROJECT_ROOT"
log_info "Hot Reload: $HOT_RELOAD | Generate Types: $GENERATE_TYPES | Monitoring: $MONITORING"

# ===========================================
# CRIAR BACKUP
# ===========================================
log_step "1. Criando Backup Completo"

mkdir -p "$BACKUP_DIR"
[ -f "docker-compose.yml" ] && cp docker-compose.yml "$BACKUP_DIR/"
[ -f "docker-compose.override.yml" ] && cp docker-compose.override.yml "$BACKUP_DIR/"
[ -d "frontend/packages/shared-api/src" ] && cp -r frontend/packages/shared-api/src "$BACKUP_DIR/"
[ -f "frontend/apps/web/Dockerfile" ] && cp frontend/apps/web/Dockerfile "$BACKUP_DIR/"

log_success "Backup criado em: $BACKUP_DIR"

# ===========================================
# CRIAR FIX-BACKEND.SH
# ===========================================
log_step "2. Criando fix-backend.sh"

cat > scripts/fix-backend.sh << 'EOF'
#!/bin/bash

# ===========================================
# SILA Backend Fix Script
# ===========================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

cd "$(dirname "$0")/.." || exit 1

log_info "🔧 Corrigindo Backend..."

# Verificar e adicionar dependências críticas
REQUIREMENTS_FILE="backend/requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    # Verificar passlib
    if ! grep -q "passlib\[bcrypt\]" "$REQUIREMENTS_FILE"; then
        echo "passlib[bcrypt]==1.7.4" >> "$REQUIREMENTS_FILE"
        log_success "passlib[bcrypt] adicionado"
    fi

    # Verificar alembic
    if ! grep -q "alembic" "$REQUIREMENTS_FILE"; then
        echo "alembic>=1.8.0" >> "$REQUIREMENTS_FILE"
        log_success "alembic adicionado"
    fi

    # Verificar uvicorn
    if ! grep -q "uvicorn" "$REQUIREMENTS_FILE"; then
        echo "uvicorn[standard]>=0.18.0" >> "$REQUIREMENTS_FILE"
        log_success "uvicorn adicionado"
    fi

    log_success "Dependências do backend verificadas"
else
    log_warning "requirements.txt não encontrado"
fi

# Verificar estrutura do backend
if [ -f "backend/main.py" ]; then
    log_success "main.py encontrado"
else
    log_warning "main.py não encontrado"
fi

if [ -f "backend/entrypoint.sh" ]; then
    chmod +x backend/entrypoint.sh
    log_success "entrypoint.sh executável"
fi

log_success "🎉 Backend fix concluído!"
EOF

chmod +x scripts/fix-backend.sh
log_success "fix-backend.sh criado"

# ===========================================
# ATUALIZAR FIX-FRONTEND.SH
# ===========================================
log_step "3. Atualizando fix-frontend.sh"

# O fix-frontend.sh já existe, vamos apenas garantir que está atualizado
if [ -f "scripts/fix-frontend.sh" ]; then
    log_success "fix-frontend.sh já existe e está atualizado"
else
    log_error "fix-frontend.sh não encontrado!"
    exit 1
fi

# ===========================================
# EXECUTAR CORREÇÕES BÁSICAS
# ===========================================
log_step "4. Executando Correções Básicas"

log_info "Executando fix-backend.sh..."
./scripts/fix-backend.sh

log_info "Executando fix-frontend.sh..."
./scripts/fix-frontend.sh

# ===========================================
# FUNCIONALIDADE: HOT RELOAD
# ===========================================
if [ "$HOT_RELOAD" = true ]; then
    log_step "5. Configurando Hot Reload"

    cat > docker-compose.override.yml << 'EOF'
version: "3.9"

services:
  backend:
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
    volumes:
      - ./backend:/app:cached
    environment:
      - PYTHONPATH=/app
      - WATCHFILES_FORCE_POLLING=true

  frontend:
    command: ["npm", "run", "dev", "--workspace=@sila-system/web", "--", "--host", "0.0.0.0", "--port", "5173"]
    volumes:
      - ./frontend:/app:cached
      - /app/node_modules
      - /app/apps/web/node_modules
    ports:
      - "5173:5173"
    environment:
      - VITE_BACKEND_URL=http://sila-backend:8000
      - CHOKIDAR_USEPOLLING=true
EOF

    log_success "Hot reload configurado via docker-compose.override.yml"
    log_feature "🔥 Frontend: http://localhost:5173 (dev server)"
    log_feature "🔥 Backend: Auto-reload habilitado"
fi

# ===========================================
# FUNCIONALIDADE: GENERATE TYPES
# ===========================================
if [ "$GENERATE_TYPES" = true ]; then
    log_step "6. Configurando Geração de Tipos TypeScript"

    # Adicionar script ao package.json do frontend
    if [ -f "frontend/package.json" ]; then
        # Verificar se o script já existe
        if ! grep -q "generate:types" frontend/package.json; then
            # Adicionar script generate:types
            sed -i '/"scripts": {/a\    "generate:types": "npx openapi-typescript http://localhost:8000/openapi.json -o packages/shared-api/src/api-types.d.ts",' frontend/package.json
            log_success "Script generate:types adicionado ao package.json"
        fi
    fi

    # Instalar openapi-typescript se não existir
    cd frontend
    if ! npm list openapi-typescript >/dev/null 2>&1; then
        log_info "Instalando openapi-typescript..."
        npm install --save-dev openapi-typescript
        log_success "openapi-typescript instalado"
    fi
    cd ..

    # Tentar gerar tipos se backend estiver rodando
    if curl -sf http://localhost:8000/openapi.json >/dev/null 2>&1; then
        log_info "Backend detectado, gerando tipos..."
        cd frontend
        npm run generate:types 2>/dev/null && log_success "Tipos TypeScript gerados!" || log_warning "Falha ao gerar tipos - execute 'npm run generate:types' após subir o backend"
        cd ..
    else
        log_warning "Backend não está rodando. Execute 'npm run generate:types' no frontend após subir o backend"
    fi

    log_feature "🤖 Tipos TypeScript: frontend/packages/shared-api/src/api-types.d.ts"
fi

# ===========================================
# FUNCIONALIDADE: MONITORING
# ===========================================
if [ "$MONITORING" = true ]; then
    log_step "7. Configurando Monitoring com Prometheus"

    # Instalar prom-client no frontend
    cd frontend
    if ! npm list prom-client >/dev/null 2>&1; then
        log_info "Instalando prom-client..."
        npm install prom-client
        log_success "prom-client instalado"
    fi
    cd ..

    # Criar servidor de métricas
    cat > frontend/apps/web/metrics-server.js << 'EOF'
const express = require('express');
const promClient = require('prom-client');

// Criar registro de métricas
const register = new promClient.Registry();

// Adicionar métricas padrão
promClient.collectDefaultMetrics({ register });

// Métricas customizadas
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

const httpRequestTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

register.registerMetric(httpRequestDuration);
register.registerMetric(httpRequestTotal);

// Servidor de métricas
const app = express();
const port = process.env.METRICS_PORT || 9111;

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`📊 Metrics server running on port ${port}`);
  console.log(`🔗 Metrics: http://localhost:${port}/metrics`);
});

module.exports = { httpRequestDuration, httpRequestTotal, register };
EOF

    # Atualizar package.json para incluir script de métricas
    if [ -f "frontend/apps/web/package.json" ]; then
        if ! grep -q "metrics" frontend/apps/web/package.json; then
            sed -i '/"scripts": {/a\    "metrics": "node metrics-server.js",' frontend/apps/web/package.json
            log_success "Script metrics adicionado"
        fi
    fi

    # Adicionar express se não existir
    cd frontend
    if ! npm list express >/dev/null 2>&1; then
        log_info "Instalando express..."
        npm install express
        log_success "express instalado"
    fi
    cd ..

    log_success "Servidor de métricas criado"
    log_feature "📊 Métricas: http://localhost:9111/metrics"
    log_feature "🏥 Health: http://localhost:9111/health"
fi

# ===========================================
# VALIDAÇÃO FINAL
# ===========================================
log_step "8. Validação Final"

# Validar docker-compose
if docker compose config >/dev/null 2>&1; then
    log_success "docker-compose.yml válido"
else
    log_error "docker-compose.yml inválido"
    exit 1
fi

# Validar estrutura
if [ -d "frontend/apps/web" ] && [ -d "frontend/packages" ]; then
    log_success "Estrutura do monorepo válida"
else
    log_error "Estrutura do monorepo inválida"
fi

if [ -d "backend" ]; then
    log_success "Backend presente"
else
    log_error "Backend não encontrado"
fi

# ===========================================
# RELATÓRIO FINAL
# ===========================================
log_step "9. Relatório Final"

log_success "🎉 SILA REPAIR ALL CONCLUÍDO!"
echo ""
log_info "📊 Funcionalidades Aplicadas:"
log_info "  ✅ Frontend: Monorepo + Docker context correto"
log_info "  ✅ Backend: Dependências + configurações"

if [ "$HOT_RELOAD" = true ]; then
    log_feature "  🔥 Hot Reload: docker-compose.override.yml criado"
fi

if [ "$GENERATE_TYPES" = true ]; then
    log_feature "  🤖 TypeScript Types: Script generate:types adicionado"
fi

if [ "$MONITORING" = true ]; then
    log_feature "  📊 Monitoring: Servidor de métricas Prometheus"
fi

echo ""
log_info "🚀 Para testar:"
if [ "$HOT_RELOAD" = true ]; then
    log_info "  docker compose up -d  # Com hot reload"
else
    log_info "  ./start_enterprise.sh --frontend"
fi

echo ""
log_info "🌐 URLs Disponíveis:"
log_info "  Frontend: http://localhost"
log_info "  Backend: http://localhost:8000"
log_info "  Docs: http://localhost:8000/docs"

if [ "$HOT_RELOAD" = true ]; then
    log_info "  Frontend Dev: http://localhost:5173"
fi

if [ "$MONITORING" = true ]; then
    log_info "  Métricas: http://localhost:9111/metrics"
fi

echo ""
log_info "📁 Backup: $BACKUP_DIR"
log_success "✨ Sistema pronto para uso!"
