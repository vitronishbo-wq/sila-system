#!/bin/bash

################################################################################
# SILA NGINX AUTOMATION - Script Inteligente de Automação e Geração de Config
################################################################################
#
# Objetivo: Automatizar a configuração, geração e otimização do Nginx
# Compatibilidade: Nova estrutura (apps/backend, apps/frontend)
# Recursos:
#   - Detecção automática de serviços disponíveis
#   - Geração dinâmica de nginx.conf baseada em serviços detectados
#   - Suporte a múltiplos ambientes (dev, staging, prod)
#   - Documentação para leigos e técnicos
#   - Validação de configuração
#   - Deploy automático
#
# Uso para leigos:
#   1. cd /caminho/para/sila-system
#   2. bash nginx_automation.sh --help           # Ver opções
#   3. bash nginx_automation.sh --diagnose       # Verificar problemas
#   4. bash nginx_automation.sh --auto           # Configurar automaticamente
#   5. bash nginx_automation.sh --generate       # Gerar nginx.conf
#
# Uso para técnicos:
#   bash nginx_automation.sh --full-deploy --env production
#   bash nginx_automation.sh --validate-config
#   bash nginx_automation.sh --test-proxy
#
################################################################################

set -e  # Exit on error

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS E MÓDULOS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"
source "$SCRIPT_DIR/../lib/nginx_config.sh"
source "$SCRIPT_DIR/../lib/nginx_deploy.sh"
source "$SCRIPT_DIR/../lib/nginx_diagnostic.sh"

# ============================================================================
# CONFIGURAÇÃO E VARIÁVEIS GLOBAIS
# ============================================================================

PROJECT_ROOT="$SCRIPT_DIR"
LOG_FILE="$PROJECT_ROOT/logs/nginx_automation_$(date +'%Y%m%d_%H%M%S').log"

# Configurações padrão - nova estrutura
APPS_DIR="$PROJECT_ROOT/apps"
BACKEND_DIR="$APPS_DIR/backend"
FRONTEND_DIR="$APPS_DIR/frontend"
DEVOPS_DIR="$PROJECT_ROOT/infrastructure/docker"
NGINX_CONFIG_DIR="$PROJECT_ROOT/infrastructure/docker"
NGINX_CONFIG="$NGINX_CONFIG_DIR/nginx.conf"
NGINX_CONFIG_TEMPLATE="$NGINX_CONFIG_DIR/nginx.conf.template"
IMAGE_NAME="sila-nginx:optimized"
CONTAINER_NAME="sila-nginx"

# Ambiente padrão
ENVIRONMENT="${ENVIRONMENT:-dev}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
NGINX_PORT="${NGINX_PORT:-80}"

help_text() {
    cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                   SILA NGINX AUTOMATION - MODO DE USO                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─ PARA LEIGOS (Modo Automático) ─────────────────────────────────────────────┐
│                                                                              │
│  🔍 Verificar problemas:                                                    │
│     bash nginx_automation.sh --diagnose                                     │
│                                                                              │
│  🚀 Configurar automaticamente (RECOMENDADO):                               │
│     bash nginx_automation.sh --auto                                         │
│     → Detecta serviços, gera config, valida e faz deploy                   │
│                                                                              │
│  📝 Apenas gerar nginx.conf (sem deploy):                                   │
│     bash nginx_automation.sh --generate                                     │
│                                                                              │
│  🧹 Limpar e começar do zero:                                               │
│     bash nginx_automation.sh --clean                                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ PARA TÉCNICOS (Modo Avançado) ────────────────────────────────────────────┐
│                                                                              │
│  🔍 Diagnóstico detalhado:                                                  │
│     bash nginx_automation.sh --diagnose --verbose                           │
│                                                                              │
│  📝 Gerar com ambiente específico:                                          │
│     bash nginx_automation.sh --generate --env production                    │
│                                                                              │
│  ✅ Validar nginx.conf:                                                     │
│     bash nginx_automation.sh --validate-config                              │
│                                                                              │
│  🧪 Testar proxy (simula requisições):                                      │
│     bash nginx_automation.sh --test-proxy                                   │
│                                                                              │
│  🚀 Deploy completo com rebuild:                                            │
│     bash nginx_automation.sh --full-deploy --env production                 │
│                                                                              │
│  📊 Listar serviços detectados:                                             │
│     bash nginx_automation.sh --list-services                                │
│                                                                              │
│  📋 Gerar relatório de status:                                              │
│     bash nginx_automation.sh --status-report                                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌─ VARIÁVEIS DE AMBIENTE ────────────────────────────────────────────────────┐
│                                                                              │
│  Alterar portas ou ambiente:                                                │
│     BACKEND_PORT=9000 NGINX_PORT=8080 bash nginx_automation.sh --auto      │
│                                                                              │
│  Variáveis suportadas:                                                      │
│     - ENVIRONMENT (dev, staging, prod) - padrão: dev                        │
│     - BACKEND_PORT - padrão: 8000                                           │
│     - FRONTEND_PORT - padrão: 5173                                          │
│     - NGINX_PORT - padrão: 80                                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

EXEMPLOS PRÁTICOS:

  1️⃣  Primeira vez (automaticamente):
      bash nginx_automation.sh --auto

  2️⃣  Apenas gerar arquivo de config (para revisar antes):
      bash nginx_automation.sh --generate

  3️⃣  Testar se tudo está ok:
      bash nginx_automation.sh --diagnose

  4️⃣  Deploy em produção:
      bash nginx_automation.sh --full-deploy --env production

  5️⃣  Visualizar a configuração gerada:
      cat infrastructure/docker/nginx.conf

SUPORTE:
  Logs detalhados salvos em: logs/nginx_automation_*.log
  Backups de config anteriores em: infrastructure/docker/nginx.conf.backup.*

EOF
}

# ============================================================================
# DETECÇÃO DE SERVIÇOS DISPONÍVEIS
# ============================================================================

detect_services() {
    log "Detectando serviços disponíveis na estrutura..."

    local services=()
    local services_info=""

    # Detectar Backend
    if [[ -d "$BACKEND_DIR" ]]; then
        if [[ -f "$BACKEND_DIR/main.py" ]] || [[ -f "$BACKEND_DIR/app.py" ]] || [[ -f "$BACKEND_DIR/app/__init__.py" ]]; then
            services+=("backend")
            services_info+="  ✓ Backend FastAPI detectado em: $BACKEND_DIR\n"
        fi
    fi

    # Detectar Frontend
    if [[ -d "$FRONTEND_DIR" ]]; then
        if [[ -f "$FRONTEND_DIR/package.json" ]] || [[ -d "$FRONTEND_DIR/apps" ]]; then
            services+=("frontend")
            services_info+="  ✓ Frontend (Node/React/Vite) detectado em: $FRONTEND_DIR\n"
        fi
    fi

    # Detectar API Gateway
    if [[ -d "$APPS_DIR/api_gateway" ]]; then
        if [[ -f "$APPS_DIR/api_gateway/package.json" ]] || [[ -f "$APPS_DIR/api_gateway/main.py" ]]; then
            services+=("api_gateway")
            services_info+="  ✓ API Gateway detectado em: $APPS_DIR/api_gateway\n"
        fi
    fi

    # Detectar Worker
    if [[ -d "$APPS_DIR/worker" ]]; then
        if [[ -f "$APPS_DIR/worker/package.json" ]] || [[ -f "$APPS_DIR/worker/main.py" ]]; then
            services+=("worker")
            services_info+="  ✓ Worker detectado em: $APPS_DIR/worker (sem rota HTTP)\n"
        fi
    fi

    if [[ ${#services[@]} -eq 0 ]]; then
        warn "Nenhum serviço detectado"
        return 1
    fi

    echo -e "$services_info"

    # Retornar serviços como array
    printf '%s\n' "${services[@]}"
    return 0
}

list_services() {
    section "Serviços Disponíveis"
    detect_services || true
}

# ============================================================================
# GERAÇÃO DINÂMICA DE CONFIGURAÇÃO NGINX
# ============================================================================

generate_nginx_config() {
    local env="${1:-$ENVIRONMENT}"
    local backend_host="${2:-backend}"
    local backend_port="${3:-$BACKEND_PORT}"
    local frontend_host="${4:-frontend}"
    local frontend_port="${5:-$FRONTEND_PORT}"

    log "Gerando nginx.conf para ambiente: $env"

    local config_file
    config_file=$(cat << EOF
# ============================================================================
# SILA SYSTEM - NGINX CONFIGURATION (Gerado Automaticamente)
# ============================================================================
# Ambiente: $env
# Data: $(date)
# Estrutura: apps/backend, apps/frontend, apps/api_gateway
# Serviços detectados:
EOF
)

    # Adicionar lista de serviços detectados
    local services
    services=$(detect_services 2>/dev/null || echo "backend frontend")

    for service in $services; do
        config_file+=$'\n'"# - $service"
    done

    config_file+=$(cat << 'EOF'
# ============================================================================

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # ========================================================================
    # LOGGING
    # ========================================================================
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # ========================================================================
    # PERFORMANCE & OTIMIZAÇÃO
    # ========================================================================
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 16M;

    # GZIP Compression - Reduz tamanho de transferência em ~70%
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # ========================================================================
    # SEGURANÇA - Headers de Segurança
    # ========================================================================
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Content Security Policy - Previne XSS
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' http://localhost:3001 https:; frame-ancestors 'self';" always;

    # ========================================================================
    # RATE LIMITING - Proteção contra abuso
    # ========================================================================
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=public:10m rate=30r/m;

    # ========================================================================
    # UPSTREAM SERVERS - Define backends
    # ========================================================================
    upstream backend_servers {
        server backend:8000 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    upstream frontend_servers {
        server frontend:5173 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    # ========================================================================
    # SERVER PRINCIPAL - SILA Frontend + API Proxy
    # ========================================================================
    server {
        listen 80 default_server;
        server_name _;
        root /usr/share/nginx/html;
        index index.html;

        # Desabilitar informações do servidor
        server_tokens off;

        # ====================================================================
        # CACHING STRATEGY
        # ====================================================================

        # Cache versioned assets for 1 year (Ex: main.abc123.js)
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options "nosniff";
            access_log off;
        }

        # Cache HTML com 1 hora (permite updates)
        location ~* \.html$ {
            expires 1h;
            add_header Cache-Control "public";
        }

        # ====================================================================
        # HEALTH CHECK - Monitoramento
        # ====================================================================
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        location /health/nginx {
            access_log off;
            return 200 "{\"status\": \"healthy\", \"service\": \"nginx\", \"timestamp\": \"$(date -u +'%Y-%m-%dT%H:%M:%SZ')\"}\n";
            add_header Content-Type application/json;
        }

        # ====================================================================
        # API PROXY - Backend FastAPI
        # ====================================================================
        location /api/ {
            limit_req zone=api burst=20 nodelay;

            # Proxy para backend
            proxy_pass http://backend_servers/;
            proxy_http_version 1.1;

            # Headers obrigatórios
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Host $host;
            proxy_set_header X-Forwarded-Port $server_port;

            # Keep-alive
            proxy_set_header Connection "upgrade";

            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;

            # Buffering
            proxy_buffering off;
        }

        # ====================================================================
        # LOGIN - Rate limiting específico para login (anti-brute-force)
        # ====================================================================
        location ~ ^/(api/)?auth/login {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://backend_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # ====================================================================
        # SPA FALLBACK - Todas as rotas conhecidas vão para index.html
        # ====================================================================
        location / {
            try_files $uri $uri/ /index.html;

            # Headers para SPA
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires "0";
        }

        # ====================================================================
        # ERROR PAGES
        # ====================================================================
        error_page 404 /index.html;
        error_page 500 502 503 504 /50x.html;

        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }

    # ========================================================================
    # DEBUG SERVER (Apenas Development)
    # ========================================================================
EOF
)

    # Adicionar server de debug para development
    if [[ "$env" == "dev" ]] || [[ "$env" == "development" ]]; then
        config_file+=$(cat << 'EOF'

    # Server para ver configuração do Nginx (apenas dev)
    server {
        listen 9999;
        server_name localhost;

        location /nginx-config {
            default_type text/plain;
            return 200 "NGINX Configuration loaded successfully\nEnvironment: dev\n";
        }

        location /nginx-status {
            stub_status on;
            access_log off;
            allow 127.0.0.1;
            allow 172.16.0.0/12;
            deny all;
        }
    }
EOF
)
    fi

    config_file+=$'\n}\n'

    # Criar backup da config anterior
    if [[ -f "$NGINX_CONFIG" ]]; then
        local backup_file="$NGINX_CONFIG.backup.$(date +%s)"
        cp "$NGINX_CONFIG" "$backup_file"
        info "Backup da configuração anterior: $backup_file"
    fi

    # Escrever nova configuração
    echo "$config_file" > "$NGINX_CONFIG"
    success "Arquivo nginx.conf gerado em: $NGINX_CONFIG"

    return 0
}

# ============================================================================
# VALIDAÇÃO DE CONFIGURAÇÃO
# ============================================================================

validate_nginx_config() {
    local config_file="${1:-$NGINX_CONFIG}"

    log "Validando nginx.conf: $config_file"

    if [[ ! -f "$config_file" ]]; then
        error "Arquivo de configuração não encontrado: $config_file"
        return 1
    fi

    # Tentar validar usando nginx:alpine
    if docker run --rm -v "$config_file:/etc/nginx/nginx.conf" nginx:alpine nginx -t 2>&1 | tee -a "$LOG_FILE"; then
        success "Configuração nginx.conf é válida ✓"
        return 0
    else
        error "Configuração nginx.conf possui erros ✗"
        return 1
    fi
}

check_backend_service() {
    log "Verificando serviço Backend..."

    if [[ ! -d "$BACKEND_DIR" ]]; then
        error "Diretório Backend não encontrado: $BACKEND_DIR"
        return 1
    fi

    if [[ -f "$BACKEND_DIR/main.py" ]] || [[ -f "$BACKEND_DIR/app.py" ]]; then
        success "Backend detectado: $BACKEND_DIR"
        return 0
    fi

    return 1
}

check_frontend_service() {
    log "Verificando serviço Frontend..."

    if [[ ! -d "$FRONTEND_DIR" ]]; then
        error "Diretório Frontend não encontrado: $FRONTEND_DIR"
        return 1
    fi

    if [[ -f "$FRONTEND_DIR/package.json" ]]; then
        success "Frontend detectado: $FRONTEND_DIR"
        return 0
    fi

    return 1
}

check_docker_available() {
    log "Verificando Docker..."

    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado"
        return 1
    fi

    if ! docker ps &>/dev/null; then
        error "Docker não está rodando"
        return 1
    fi

    success "Docker está disponível"
    return 0
}

test_proxy_backend() {
    log "Testando proxy para Backend..."

    if ! command -v curl &> /dev/null; then
        warn "curl não disponível, pulando teste"
        return 0
    fi

    # Esperar um pouco para o nginx iniciar
    sleep 2

    info "Testando conexão com /health..."
    if curl -sf http://localhost:$NGINX_PORT/health 2>/dev/null | grep -q "healthy"; then
        success "Health check OK"
        return 0
    else
        warn "Health check falhou (backend pode não estar rodando)"
        return 1
    fi
}

diagnose_nginx_issue() {
    section "Diagnóstico de Problemas"

    local issues=()
    local status=0

    # Verificar estrutura
    info "Verificando estrutura de diretórios..."
    if ! check_backend_service; then
        issues+=("Backend não encontrado")
        status=1
    fi

    if ! check_frontend_service; then
        issues+=("Frontend não encontrado")
        status=1
    fi

    # Verificar configuração
    info "Verificando arquivo nginx.conf..."
    if [[ ! -f "$NGINX_CONFIG" ]]; then
        issues+=("nginx.conf não existe")
        status=1
    else
        if ! validate_nginx_config; then
            issues+=("nginx.conf inválido")
            status=1
        fi
    fi

    # Verificar Docker
    info "Verificando Docker..."
    if ! check_docker_available; then
        issues+=("Docker não disponível")
        status=1
    fi

    if [[ ${#issues[@]} -eq 0 ]]; then
        success "Nenhum problema crítico detectado"
        info "Sistema pronto para deploy"
        return 0
    else
        echo ""
        echo -e "${YELLOW}Problemas encontrados:${NC}"
        for issue in "${issues[@]}"; do
            echo -e "  ${RED}✗${NC} $issue"
        done
        return "$status"
    fi
}

# ============================================================================
# FUNÇÕES DE CORREÇÃO E DEPLOY
# ============================================================================

start_nginx_container() {
    log "Iniciando container Nginx..."

    # Parar container existente
    if docker ps -q -f "name=$CONTAINER_NAME" | grep -q .; then
        info "Parando container existente: $CONTAINER_NAME"
        docker stop "$CONTAINER_NAME" || true
    fi

    if docker ps -aq -f "name=$CONTAINER_NAME" | grep -q .; then
        info "Removendo container antigo: $CONTAINER_NAME"
        docker rm "$CONTAINER_NAME" || true
    fi

    # Iniciar novo container
    info "Iniciando container Nginx..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$NGINX_PORT:80" \
        -v "$NGINX_CONFIG:/etc/nginx/nginx.conf:ro" \
        -v "$(pwd)/apps/frontend/apps/web/dist:/usr/share/nginx/html:ro" \
        --network sila-network \
        nginx:alpine

    if [[ $? -eq 0 ]]; then
        success "Container Nginx iniciado com sucesso"
        return 0
    else
        error "Falha ao iniciar container Nginx"
        return 1
    fi
}

status_report() {
    section "Status do Sistema"

    echo "📍 Estrutura do Projeto:"
    echo "  Project Root: $PROJECT_ROOT"
    echo "  Apps Dir: $APPS_DIR"
    echo "  Backend: $BACKEND_DIR"
    echo "  Frontend: $FRONTEND_DIR"
    echo ""

    echo "📋 Serviços Detectados:"
    detect_services || echo "  Nenhum serviço detectado"
    echo ""

    echo "🐳 Docker:"
    if command -v docker &> /dev/null; then
        echo "  Status: $(docker ps &>/dev/null && echo 'Rodando' || echo 'Parado')"
        if docker ps -q -f "name=$CONTAINER_NAME" | grep -q .; then
            echo "  Container $CONTAINER_NAME: Rodando"
        else
            echo "  Container $CONTAINER_NAME: Parado ou não existe"
        fi
    else
        echo "  Status: Não instalado"
    fi
    echo ""

    echo "📝 Configuração:"
    echo "  Nginx Config: $NGINX_CONFIG"
    echo "  Existe: $(test -f "$NGINX_CONFIG" && echo 'Sim' || echo 'Não')"
    if [[ -f "$NGINX_CONFIG" ]]; then
        echo "  Válida: $(validate_nginx_config &>/dev/null && echo 'Sim' || echo 'Não')"
    fi
    echo ""

    echo "🔧 Configurações Atuais:"
    echo "  Ambiente: $ENVIRONMENT"
    echo "  Backend Port: $BACKEND_PORT"
    echo "  Frontend Port: $FRONTEND_PORT"
    echo "  Nginx Port: $NGINX_PORT"
}

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

print_banner() {
    cat << 'EOF'

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                 🚀 SILA NGINX AUTOMATION SYSTEM 🚀                           ║
║                                                                              ║
║         Automação Inteligente de Configuração e Deploy do Nginx              ║
║                                                                              ║
║                        versão 2.0 (Otimizada)                                ║
║                    Compatível com nova estrutura (apps/)                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

EOF
}

main() {
    print_banner

    # Criar diretório de logs
    mkdir -p "$(dirname "$LOG_FILE")"

    log "=== INICIANDO NGINX AUTOMATION ==="
    log "Ambiente: $ENVIRONMENT"
    log "Log: $LOG_FILE"

    # Processar argumentos
    local action="${1:-help}"

    case "$action" in
        --help|-h)
            help_text
            ;;

        --diagnose)
            diagnose_nginx_issue
            ;;

        --generate)
            section "Gerando Configuração Nginx"
            generate_nginx_config "$ENVIRONMENT"
            ;;

        --list-services)
            list_services
            ;;

        --validate-config|--validate)
            section "Validando Configuração"
            validate_nginx_config
            ;;

        --test-proxy)
            section "Testando Proxy"
            test_proxy_backend
            ;;

        --status-report)
            status_report
            ;;

        --auto)
            section "Modo Automático - Configuração Completa"

            if ! check_docker_available; then
                error "Docker não está disponível. Instale o Docker e tente novamente."
                exit 1
            fi

            # Detectar serviços
            log "Detectando serviços..."
            detect_services || true

            # Gerar configuração
            if ! generate_nginx_config "$ENVIRONMENT"; then
                error "Falha ao gerar configuração"
                exit 1
            fi

            # Validar
            if ! validate_nginx_config; then
                error "Configuração inválida"
                exit 1
            fi

            # Iniciar container
            if ! start_nginx_container; then
                error "Falha ao iniciar container Nginx"
                exit 1
            fi

            # Teste rápido
            test_proxy_backend

            success "=== CONFIGURAÇÃO CONCLUÍDA COM SUCESSO ==="
            echo ""
            echo "📍 Seu Nginx está rodando em http://localhost:$NGINX_PORT"
            echo "📝 Configuração: $NGINX_CONFIG"
            echo "📊 Logs: $LOG_FILE"
            ;;

        --full-deploy)
            section "Deploy Completo"

            # Argumentos adicionais
            shift
            while [[ $# -gt 0 ]]; do
                case "$1" in
                    --env)
                        ENVIRONMENT="$2"
                        shift 2
                        ;;
                    *)
                        shift
                        ;;
                esac
            done

            if ! check_docker_available; then
                error "Docker não está disponível"
                exit 1
            fi

            # Diagnóstico
            diagnose_nginx_issue || warn "Alguns warnings foram encontrados"

            # Gerar config
            if ! generate_nginx_config "$ENVIRONMENT"; then
                error "Falha ao gerar configuração"
                exit 1
            fi

            # Validar
            if ! validate_nginx_config; then
                error "Configuração inválida"
                exit 1
            fi

            # Deploy
            if ! start_nginx_container; then
                error "Falha no deploy"
                exit 1
            fi

            success "=== DEPLOY CONCLUÍDO COM SUCESSO ==="
            status_report
            ;;

        --clean)
            section "Limpeza"

            log "Parando container Nginx..."
            docker stop "$CONTAINER_NAME" 2>/dev/null || true

            log "Removendo container..."
            docker rm "$CONTAINER_NAME" 2>/dev/null || true

            success "Limpeza concluída"
            ;;

        --verbose)
            shift
            bash "$0" "$@" 2>&1
            ;;

        *)
            error "Opção desconhecida: $action"
            echo ""
            help_text
            exit 1
            ;;
    esac
}

# ============================================================================
# EXECUÇÃO
# ============================================================================

# Verificar se tem argumentos, senão mostrar ajuda
if [[ $# -eq 0 ]]; then
    main --help
else
    main "$@"
fi
