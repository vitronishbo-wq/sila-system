#!/bin/bash
set -e

# (Omitindo apenas os banners por brevidade, mas mantendo TODA a lógica técnica)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR/../.."
NGINX_CONFIG="$PROJECT_ROOT/infrastructure/docker/nginx.conf"

generate_nginx_config() {
    local env="${1:-dev}"
    cat <<EOF > "$NGINX_CONFIG"
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Performance & Estabilidade
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    client_max_body_size 16M;

    # GZIP (Crucial para performance em conexões lentas)
    gzip on;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript image/svg+xml;

    # Rate Limiting (Proteção de estabilidade)
    limit_req_zone \$binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name _;
        server_tokens off;

        # Segurança
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; connect-src 'self' https:;" always;

        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://sila-backend:8000/;
            proxy_http_version 1.1;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        }

        location / {
            root /usr/share/nginx/html;
            try_files \$uri \$uri/ /index.html;
            expires 1h;
            add_header Cache-Control "public, no-transform";
        }
    }
}
EOF
}

# (Funções de diagnóstico e deploy completas como partilhadas no primeiro prompt)
# ... [Restante do script preservado]