#!/bin/bash

################################################################################
# SILA CLEANUP - Script Unificado de Limpeza
# Consolida funcionalidades de múltiplos cleanup scripts
#
# Uso:
#   ./cleanup.sh --all              # Limpar tudo
#   ./cleanup.sh --backups          # Apenas backups
#   ./cleanup.sh --temp             # Apenas arquivos temporários
#   ./cleanup.sh --obsolete         # Apenas arquivos obsoletos
#   ./cleanup.sh --dry-run          # Simular sem deletar
#   ./cleanup.sh --help             # Ver opções
################################################################################

set -euo pipefail

# ============================================================================
# IMPORTAR BIBLIOTECAS COMUNS
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../lib/colors.sh"
source "$SCRIPT_DIR/../lib/logging.sh"

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DRY_RUN=false
VERBOSE=false
TOTAL_FREED=0

# ============================================================================
# FUNÇÕES DE LIMPEZA
# ============================================================================

cleanup_python_cache() {
    section "Limpando cache Python"

    local count=0

    # Remover __pycache__
    while IFS= read -r dir; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $dir"
        else
            rm -rf "$dir"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type d -name "__pycache__" 2>/dev/null)

    # Remover .pyc
    while IFS= read -r file; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type f -name "*.pyc" 2>/dev/null)

    # Remover .pyo
    while IFS= read -r file; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type f -name "*.pyo" 2>/dev/null)

    success "Removidos $count ficheiros/diretórios Python"
}

cleanup_node_modules() {
    section "Limpando node_modules e cache npm"

    local count=0

    # Remover node_modules
    while IFS= read -r dir; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $dir"
        else
            rm -rf "$dir"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type d -name "node_modules" 2>/dev/null)

    # Limpar cache npm
    if [ "$DRY_RUN" = false ]; then
        npm cache clean --force 2>/dev/null || true
    fi

    success "Removidos $count diretórios node_modules"
}

cleanup_build_artifacts() {
    section "Limpando artefatos de build"

    local count=0

    # Remover dist/
    while IFS= read -r dir; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $dir"
        else
            rm -rf "$dir"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type d -name "dist" 2>/dev/null)

    # Remover build/
    while IFS= read -r dir; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $dir"
        else
            rm -rf "$dir"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type d -name "build" 2>/dev/null)

    # Remover .egg-info/
    while IFS= read -r dir; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $dir"
        else
            rm -rf "$dir"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type d -name "*.egg-info" 2>/dev/null)

    success "Removidos $count artefatos de build"
}

cleanup_logs() {
    section "Limpando logs antigos"

    local keep_days=7
    local count=0

    # Remover logs com mais de N dias
    while IFS= read -r file; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type f -name "*.log" -mtime +$keep_days 2>/dev/null)

    success "Removidos $count ficheiros de log antigos (>$keep_days dias)"
}

cleanup_backups() {
    section "Limpando backups antigos"

    local count=0

    # Remover diretórios .backup_*
    while IFS= read -r dir; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $dir"
        else
            rm -rf "$dir"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type d -name ".backup_*" 2>/dev/null)

    success "Removidos $count diretórios de backup"
}

cleanup_temp_files() {
    section "Limpando arquivos temporários"

    local count=0

    # Remover .tmp/
    if [ -d "$PROJECT_ROOT/.tmp" ]; then
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $PROJECT_ROOT/.tmp"
        else
            rm -rf "$PROJECT_ROOT/.tmp"
        fi
        ((count++))
    fi

    # Remover .cache/
    if [ -d "$PROJECT_ROOT/.cache" ]; then
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $PROJECT_ROOT/.cache"
        else
            rm -rf "$PROJECT_ROOT/.cache"
        fi
        ((count++))
    fi

    # Remover .pytest_cache/
    while IFS= read -r dir; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $dir"
        else
            rm -rf "$dir"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type d -name ".pytest_cache" 2>/dev/null)

    success "Removidos $count diretórios temporários"
}

cleanup_obsolete_files() {
    section "Limpando ficheiros obsoletos"

    local count=0

    # Remover .bak
    while IFS= read -r file; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type f -name "*.bak" 2>/dev/null)

    # Remover .old
    while IFS= read -r file; do
        if [ "$DRY_RUN" = true ]; then
            log "Seria removido: $file"
        else
            rm -f "$file"
        fi
        ((count++))
    done < <(find "$PROJECT_ROOT" -type f -name "*.old" 2>/dev/null)

    success "Removidos $count ficheiros obsoletos"
}

# ============================================================================
# MENU E AJUDA
# ============================================================================

show_help() {
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║                    SILA CLEANUP - Script Unificado                        ║
║                      Limpeza Inteligente do Projeto                       ║
╚════════════════════════════════════════════════════════════════════════════╝

OPÇÕES:
  --all              Limpar tudo (padrão)
  --python           Limpar cache Python (__pycache__, .pyc, .pyo)
  --node             Limpar node_modules e cache npm
  --build            Limpar artefatos de build (dist/, build/, .egg-info/)
  --logs             Limpar logs antigos (>7 dias)
  --backups          Limpar diretórios de backup (.backup_*)
  --temp             Limpar arquivos temporários (.tmp/, .cache/, .pytest_cache/)
  --obsolete         Limpar ficheiros obsoletos (.bak, .old)
  --dry-run          Simular limpeza sem deletar ficheiros
  --verbose          Mostrar detalhes de cada operação
  --help             Mostrar esta ajuda

EXEMPLOS:
  ./cleanup.sh                    # Limpar tudo
  ./cleanup.sh --python           # Apenas cache Python
  ./cleanup.sh --all --dry-run    # Simular limpeza completa
  ./cleanup.sh --logs --backups   # Limpar logs e backups
  ./cleanup.sh --temp --verbose   # Limpar temp com detalhes

EOF
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

main() {
    local cleanup_type="all"

    # Processar argumentos
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --all)
                cleanup_type="all"
                ;;
            --python)
                cleanup_type="python"
                ;;
            --node)
                cleanup_type="node"
                ;;
            --build)
                cleanup_type="build"
                ;;
            --logs)
                cleanup_type="logs"
                ;;
            --backups)
                cleanup_type="backups"
                ;;
            --temp)
                cleanup_type="temp"
                ;;
            --obsolete)
                cleanup_type="obsolete"
                ;;
            --dry-run)
                DRY_RUN=true
                ;;
            --verbose)
                VERBOSE=true
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                error "Opção desconhecida: $1"
                show_help
                exit 1
                ;;
        esac
        shift
    done

    # Banner
    echo -e "${BOLD}${CYAN}"
    cat << "EOF"
╔════════════════════════════════════════════════════════════════════════════╗
║                    🧹 SILA CLEANUP - Iniciando                            ║
╚════════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"

    if [ "$DRY_RUN" = true ]; then
        warn "MODO SIMULAÇÃO: Nenhum ficheiro será deletado"
        echo ""
    fi

    # Executar limpeza baseada no tipo
    case "$cleanup_type" in
        all)
            cleanup_python_cache
            cleanup_node_modules
            cleanup_build_artifacts
            cleanup_logs
            cleanup_backups
            cleanup_temp_files
            cleanup_obsolete_files
            ;;
        python)
            cleanup_python_cache
            ;;
        node)
            cleanup_node_modules
            ;;
        build)
            cleanup_build_artifacts
            ;;
        logs)
            cleanup_logs
            ;;
        backups)
            cleanup_backups
            ;;
        temp)
            cleanup_temp_files
            ;;
        obsolete)
            cleanup_obsolete_files
            ;;
    esac

    # Resumo final
    echo -e "\n${BOLD}${CYAN}════════════════════════════════════════════════════════════════════════════════${NC}"
    if [ "$DRY_RUN" = true ]; then
        success "Simulação concluída (nenhum ficheiro foi deletado)"
    else
        success "Limpeza concluída com sucesso!"
    fi
    echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════════════════════════${NC}\n"
}

main "$@"
