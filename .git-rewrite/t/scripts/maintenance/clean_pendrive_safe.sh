#!/bin/bash

# =================================================================
# Script de Limpeza Segura do Pendrive (Sistema Live)
# Remove apenas arquivos temporários sem afetar o sistema live
# =================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Function to safely clean temporary directories
clean_temp_safely() {
    log_info "Iniciando limpeza segura do sistema..."

    # Clean user temporary files (if writable)
    if [ -d "/tmp" ] && mount | grep -q "/tmp"; then
        log_info "Limpando diretório /tmp..."
        # Remove only files older than 1 day to be safe
        find /tmp -type f -mtime +1 -delete 2>/dev/null || true
        log_success "Arquivos temporários antigos removidos de /tmp"
    fi

    # Clean user cache (if writable and not system critical)
    if [ -d "/var/cache" ]; then
        log_info "Verificando cache do sistema..."
        # Only clean specific non-critical caches
        rm -rf /var/cache/apt/archives/partial/* 2>/dev/null || true
        log_info "Cache APT parcial limpo"
    fi

    # Clean Docker temporary files (if Docker data dir exists)
    if [ -d "/var/lib/docker/tmp" ]; then
        log_info "Limpando cache temporário do Docker..."
        rm -rf /var/lib/docker/tmp/* 2>/dev/null || true
        log_success "Cache Docker temporário limpo"
    fi

    # Clean journal logs older than 7 days (if writable)
    if command -v journalctl &> /dev/null; then
        log_info "Limpando logs antigos do journal..."
        journalctl --vacuum-time=7d 2>/dev/null || true
        log_success "Logs antigos do journal removidos"
    fi

    # Clean thumbnail cache (if exists)
    if [ -d "/home/mint/.cache/thumbnails" ]; then
        log_info "Limpando cache de thumbnails..."
        rm -rf /home/mint/.cache/thumbnails/* 2>/dev/null || true
        log_success "Cache de thumbnails limpo"
    fi

    log_success "Limpeza segura concluída!"
}

# Function to show disk usage before and after
show_disk_usage() {
    log_info "Uso de disco atual:"
    df -h | grep -E "(Filesystem|/dev/)" | head -10
    echo ""
}

# Function to check available space
check_available_space() {
    log_info "Verificando espaço disponível..."

    # Check root filesystem
    ROOT_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$ROOT_USAGE" -gt 80 ]; then
        log_warning "Sistema raiz com uso alto: ${ROOT_USAGE}%"
    else
        log_info "Sistema raiz: ${ROOT_USAGE}% usado"
    fi

    # Check tmp directory if separate
    if mount | grep -q "/tmp"; then
        TMP_USAGE=$(df /tmp | awk 'NR==2 {print $5}' | sed 's/%//')
        log_info "Diretório /tmp: ${TMP_USAGE}% usado"
    fi
}

# Main execution
main() {
    echo "================================================================="
    echo "        LIMPEZA SEGURA DO PENDRIVE (SISTEMA LIVE)"
    echo "================================================================="
    echo ""

    # Show initial disk usage
    show_disk_usage

    # Check current space
    check_available_space

    # Ask for confirmation
    echo ""
    read -p "⚠️  Esta operação irá remover arquivos temporários. Continuar? (s/N): " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        log_info "Operação cancelada pelo usuário"
        exit 0
    fi

    # Perform safe cleaning
    clean_temp_safely

    # Show final disk usage
    echo ""
    show_disk_usage

    log_success "✅ Limpeza concluída com segurança!"
    log_info "O sistema live não foi afetado."
    log_info "Para mais espaço, considere:"
    echo "  - Desmontar dispositivos externos não utilizados"
    echo "  - Limpar containers Docker parados: docker system prune"
    echo "  - Remover imagens Docker não utilizadas: docker image prune"
}

# Run main function
main "$@"
