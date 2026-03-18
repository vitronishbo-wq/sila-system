#!/bin/bash

################################################################################
# NGINX DEPLOY MODULE - Deploy e Gerenciamento de Container
# Módulo para nginx_automation.sh
################################################################################

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/colors.sh"
source "$SCRIPT_DIR/logging.sh"

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

NGINX_IMAGE="${NGINX_IMAGE:-sila-nginx:optimized}"
NGINX_CONTAINER="${NGINX_CONTAINER:-sila-nginx}"
NGINX_PORT="${NGINX_PORT:-80}"

# ============================================================================
# FUNÇÕES DE BUILD
# ============================================================================

build_nginx_image() {
    local dockerfile="${1:-Dockerfile}"
    local tag="${2:-$NGINX_IMAGE}"

    section "Construindo imagem Nginx: $tag"

    if [ ! -f "$dockerfile" ]; then
        error "Dockerfile não encontrado: $dockerfile"
        return 1
    fi

    if docker build -f "$dockerfile" -t "$tag" .; then
        success "Imagem construída com sucesso: $tag"
        return 0
    else
        error "Falha ao construir imagem"
        return 1
    fi
}

# ============================================================================
# FUNÇÕES DE DEPLOY
# ============================================================================

deploy_nginx_container() {
    local image="${1:-$NGINX_IMAGE}"
    local container="${2:-$NGINX_CONTAINER}"
    local port="${3:-$NGINX_PORT}"

    section "Fazendo deploy do container Nginx"

    # Parar container existente
    if docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
        log "Parando container existente: $container"
        docker stop "$container" 2>/dev/null || true
        docker rm "$container" 2>/dev/null || true
    fi

    # Iniciar novo container
    log "Iniciando novo container: $container"
    if docker run -d \
        --name "$container" \
        -p "$port:80" \
        -v "$(pwd)/infrastructure/docker/nginx.conf:/etc/nginx/nginx.conf:ro" \
        -v "$(pwd)/infrastructure/docker/ssl:/etc/nginx/ssl:ro" \
        --restart unless-stopped \
        "$image"; then
        success "Container iniciado com sucesso"
        return 0
    else
        error "Falha ao iniciar container"
        return 1
    fi
}

# ============================================================================
# FUNÇÕES DE GERENCIAMENTO
# ============================================================================

restart_nginx() {
    local container="${1:-$NGINX_CONTAINER}"

    section "Reiniciando Nginx"

    if docker restart "$container"; then
        success "Nginx reiniciado com sucesso"
        return 0
    else
        error "Falha ao reiniciar Nginx"
        return 1
    fi
}

reload_nginx_config() {
    local container="${1:-$NGINX_CONTAINER}"

    section "Recarregando configuração Nginx"

    if docker exec "$container" nginx -s reload; then
        success "Configuração recarregada com sucesso"
        return 0
    else
        error "Falha ao recarregar configuração"
        return 1
    fi
}

stop_nginx() {
    local container="${1:-$NGINX_CONTAINER}"

    section "Parando Nginx"

    if docker stop "$container"; then
        success "Nginx parado com sucesso"
        return 0
    else
        error "Falha ao parar Nginx"
        return 1
    fi
}

# ============================================================================
# FUNÇÕES DE MONITORAMENTO
# ============================================================================

check_nginx_status() {
    local container="${1:-$NGINX_CONTAINER}"

    section "Verificando status do Nginx"

    if docker ps --filter "name=$container" --filter "status=running" | grep -q "$container"; then
        success "Container Nginx está rodando"

        # Mostrar informações
        log "Informações do container:"
        docker ps --filter "name=$container" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

        return 0
    else
        warn "Container Nginx não está rodando"
        return 1
    fi
}

show_nginx_logs() {
    local container="${1:-$NGINX_CONTAINER}"
    local lines="${2:-50}"

    section "Últimas $lines linhas de log do Nginx"

    docker logs --tail "$lines" "$container"
}

get_nginx_stats() {
    local container="${1:-$NGINX_CONTAINER}"

    section "Estatísticas do container Nginx"

    docker stats "$container" --no-stream
}

# ============================================================================
# FUNÇÕES DE BACKUP
# ============================================================================

backup_nginx_config() {
    local config_file="${1:-infrastructure/docker/nginx.conf}"
    local backup_dir="${2:-.backup_nginx}"

    section "Fazendo backup da configuração Nginx"

    mkdir -p "$backup_dir"

    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local backup_file="$backup_dir/nginx.conf.$timestamp"

    if cp "$config_file" "$backup_file"; then
        success "Backup criado: $backup_file"
        return 0
    else
        error "Falha ao criar backup"
        return 1
    fi
}

# ============================================================================
# EXPORTAR FUNÇÕES
# ============================================================================

export -f build_nginx_image
export -f deploy_nginx_container
export -f restart_nginx
export -f reload_nginx_config
export -f stop_nginx
export -f check_nginx_status
export -f show_nginx_logs
export -f get_nginx_stats
export -f backup_nginx_config
