#!/bin/bash

################################################################################
# NGINX CONFIG MODULE - Geração e Validação de Configuração
# Módulo para nginx_automation.sh
################################################################################

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/colors.sh"
source "$SCRIPT_DIR/logging.sh"

# ============================================================================
# FUNÇÕES DE DETECÇÃO DE SERVIÇOS
# ============================================================================

detect_services() {
    section "Detectando serviços disponíveis"

    local services=()

    # Detectar backend
    if [ -d "apps/backend" ]; then
        services+=("backend")
        log "Backend detectado em apps/backend"
    fi

    # Detectar frontend
    if [ -d "apps/frontend" ]; then
        services+=("frontend")
        log "Frontend detectado em apps/frontend"
    fi

    # Detectar worker
    if [ -d "apps/worker" ]; then
        services+=("worker")
        log "Worker detectado em apps/worker"
    fi

    # Detectar API Gateway
    if [ -d "apps/api_gateway" ]; then
        services+=("api_gateway")
        log "API Gateway detectado em apps/api_gateway"
    fi

    if [ ${#services[@]} -eq 0 ]; then
        warn "Nenhum serviço detectado"
        return 1
    fi

    success "Detectados ${#services[@]} serviços: ${services[*]}"
    echo "${services[@]}"
}

# ============================================================================
# FUNÇÕES DE GERAÇÃO DE CONFIG
# ============================================================================

generate_nginx_config() {
    local env="${1:-dev}"
    local output_file="${2:-nginx.conf}"

    section "Gerando nginx.conf para ambiente: $env"

    cat > "$output_file" << 'EOF'
# ============================================================================
# SILA NGINX CONFIGURATION - Auto-generated
# ============================================================================

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;

    # Upstream backends
    upstream backend {
        least_conn;
        server backend:8000 max_fails=3 fail_timeout=30s;
    }

    upstream frontend {
        least_conn;
        server frontend:5173 max_fails=3 fail_timeout=30s;
    }

    # HTTP redirect to HTTPS (production only)
    server {
        listen 80;
        server_name _;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    # Main HTTPS server
    server {
        listen 443 ssl http2;
        server_name _;

        # SSL configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=50 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 30s;
        }

        # Health check endpoint
        location /health {
            access_log off;
            proxy_pass http://backend;
            proxy_set_header Host $host;
        }

        # Metrics endpoint (internal only)
        location /metrics {
            allow 127.0.0.1;
            allow 172.16.0.0/12;
            deny all;
            proxy_pass http://backend;
            proxy_set_header Host $host;
        }

        # Frontend
        location / {
            limit_req zone=general burst=20 nodelay;
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Static files caching
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
EOF

    success "nginx.conf gerado em $output_file"
}

# ============================================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================================

validate_nginx_config() {
    local config_file="${1:-nginx.conf}"

    section "Validando configuração Nginx"

    if [ ! -f "$config_file" ]; then
        error "Ficheiro de configuração não encontrado: $config_file"
        return 1
    fi

    # Validar sintaxe com nginx -t
    if command -v nginx &> /dev/null; then
        if nginx -t -c "$(pwd)/$config_file" 2>&1 | grep -q "successful"; then
            success "Configuração Nginx válida"
            return 0
        else
            error "Configuração Nginx inválida"
            nginx -t -c "$(pwd)/$config_file"
            return 1
        fi
    else
        warn "nginx não instalado, pulando validação"
        return 0
    fi
}

# ============================================================================
# FUNÇÕES DE TESTE
# ============================================================================

test_nginx_proxy() {
    section "Testando proxy Nginx"

    local backend_url="${1:-http://localhost:8000}"
    local frontend_url="${2:-http://localhost:5173}"

    log "Testando backend em $backend_url..."
    if curl -f -s "$backend_url/health" > /dev/null; then
        success "Backend respondendo corretamente"
    else
        warn "Backend não respondendo em $backend_url"
    fi

    log "Testando frontend em $frontend_url..."
    if curl -f -s "$frontend_url" > /dev/null; then
        success "Frontend respondendo corretamente"
    else
        warn "Frontend não respondendo em $frontend_url"
    fi
}

# ============================================================================
# EXPORTAR FUNÇÕES
# ============================================================================

export -f detect_services
export -f generate_nginx_config
export -f validate_nginx_config
export -f test_nginx_proxy
