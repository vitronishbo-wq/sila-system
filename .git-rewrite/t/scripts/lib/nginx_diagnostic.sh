#!/bin/bash

################################################################################
# NGINX DIAGNOSTIC MODULE - Diagnóstico e Troubleshooting
# Módulo para nginx_automation.sh
################################################################################

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/colors.sh"
source "$SCRIPT_DIR/logging.sh"

# ============================================================================
# FUNÇÕES DE DIAGNÓSTICO
# ============================================================================

diagnose_system() {
    section "Diagnóstico do Sistema"

    # Verificar Docker
    log "Verificando Docker..."
    if command -v docker &> /dev/null; then
        success "Docker instalado: $(docker --version)"
    else
        error "Docker não instalado"
        return 1
    fi

    # Verificar Docker Compose
    log "Verificando Docker Compose..."
    if docker compose version &> /dev/null; then
        success "Docker Compose instalado: $(docker compose version | head -1)"
    elif command -v docker-compose &> /dev/null; then
        success "docker-compose instalado: $(docker-compose --version)"
    else
        error "Docker Compose não instalado"
        return 1
    fi

    # Verificar espaço em disco
    log "Verificando espaço em disco..."
    local free_space=$(df -h . | awk 'NR==2 {print $4}')
    success "Espaço livre: $free_space"

    # Verificar memória
    log "Verificando memória disponível..."
    local free_mem=$(free -h | awk 'NR==2 {print $7}')
    success "Memória livre: $free_mem"

    return 0
}

# ============================================================================
# FUNÇÕES DE VERIFICAÇÃO DE DEPENDÊNCIAS
# ============================================================================

check_dependencies() {
    section "Verificando Dependências"

    local missing=()
    local commands=("docker" "curl" "grep" "sed" "awk")

    for cmd in "${commands[@]}"; do
        if command -v "$cmd" &> /dev/null; then
            success "$cmd instalado"
        else
            error "$cmd não instalado"
            missing+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        error "Dependências faltando: ${missing[*]}"
        return 1
    fi

    success "Todas as dependências verificadas"
    return 0
}

# ============================================================================
# FUNÇÕES DE TESTE DE CONECTIVIDADE
# ============================================================================

test_connectivity() {
    section "Testando Conectividade"

    local backend_url="${1:-http://localhost:8000}"
    local frontend_url="${2:-http://localhost:5173}"
    local nginx_url="${3:-http://localhost}"

    # Teste backend
    log "Testando backend: $backend_url"
    if curl -f -s -m 5 "$backend_url/health" > /dev/null 2>&1; then
        success "Backend respondendo"
    else
        warn "Backend não respondendo"
    fi

    # Teste frontend
    log "Testando frontend: $frontend_url"
    if curl -f -s -m 5 "$frontend_url" > /dev/null 2>&1; then
        success "Frontend respondendo"
    else
        warn "Frontend não respondendo"
    fi

    # Teste Nginx
    log "Testando Nginx: $nginx_url"
    if curl -f -s -m 5 "$nginx_url" > /dev/null 2>&1; then
        success "Nginx respondendo"
    else
        warn "Nginx não respondendo"
    fi
}

# ============================================================================
# FUNÇÕES DE ANÁLISE DE LOGS
# ============================================================================

analyze_nginx_logs() {
    local container="${1:-sila-nginx}"
    local lines="${2:-100}"

    section "Analisando logs do Nginx"

    log "Últimas $lines linhas:"
    docker logs --tail "$lines" "$container" 2>/dev/null | tail -20

    log "Erros encontrados:"
    docker logs "$container" 2>/dev/null | grep -i "error" | tail -10 || log "Nenhum erro encontrado"

    log "Avisos encontrados:"
    docker logs "$container" 2>/dev/null | grep -i "warn" | tail -10 || log "Nenhum aviso encontrado"
}

# ============================================================================
# FUNÇÕES DE RELATÓRIO
# ============================================================================

generate_diagnostic_report() {
    local output_file="${1:-nginx_diagnostic_report.txt}"

    section "Gerando Relatório de Diagnóstico"

    {
        echo "╔════════════════════════════════════════════════════════════════╗"
        echo "║         RELATÓRIO DE DIAGNÓSTICO - SILA NGINX                 ║"
        echo "║         Gerado em: $(date)                          ║"
        echo "╚════════════════════════════════════════════════════════════════╝"
        echo ""

        echo "📊 INFORMAÇÕES DO SISTEMA"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Hostname: $(hostname)"
        echo "Kernel: $(uname -r)"
        echo "Uptime: $(uptime -p)"
        echo ""

        echo "🐳 INFORMAÇÕES DO DOCKER"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        docker --version
        docker compose version 2>/dev/null || docker-compose --version
        echo ""

        echo "📦 CONTAINERS EM EXECUÇÃO"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""

        echo "🖼️  IMAGENS DISPONÍVEIS"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        docker images | grep -E "nginx|sila" || echo "Nenhuma imagem nginx/sila encontrada"
        echo ""

        echo "💾 USO DE DISCO"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        df -h
        echo ""

        echo "🧠 USO DE MEMÓRIA"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        free -h
        echo ""

    } | tee "$output_file"

    success "Relatório salvo em: $output_file"
}

# ============================================================================
# FUNÇÕES DE TROUBLESHOOTING
# ============================================================================

troubleshoot_nginx() {
    section "Troubleshooting Nginx"

    local container="${1:-sila-nginx}"

    # Verificar se container existe
    if ! docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
        error "Container não encontrado: $container"
        return 1
    fi

    # Verificar se está rodando
    if ! docker ps --filter "name=$container" --filter "status=running" | grep -q "$container"; then
        warn "Container não está rodando"
        log "Tentando iniciar..."
        docker start "$container"
    fi

    # Verificar logs
    log "Últimos erros:"
    docker logs "$container" 2>&1 | grep -i "error" | tail -5 || log "Nenhum erro"

    # Verificar configuração
    log "Validando configuração Nginx..."
    docker exec "$container" nginx -t 2>&1 || warn "Configuração inválida"

    success "Troubleshooting concluído"
}

# ============================================================================
# EXPORTAR FUNÇÕES
# ============================================================================

export -f diagnose_system
export -f check_dependencies
export -f test_connectivity
export -f analyze_nginx_logs
export -f generate_diagnostic_report
export -f troubleshoot_nginx
