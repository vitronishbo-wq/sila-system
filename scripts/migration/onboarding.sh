#!/bin/bash
################################################################################
# 🚀 SILA System - Onboarding Master Script
# Orquestra a sequência completa: análise → classificação → migração → validação
# Gera relatório final com antes/depois
#
# Uso:
#   ./onboarding.sh                    # Executar tudo
#   ./onboarding.sh --phase 1          # Apenas Fase 1
#   ./onboarding.sh --dry-run          # Sem modificar arquivos
#   ./onboarding.sh --interactive      # Menu interativo
################################################################################

set -euo pipefail

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

BACKEND_PATH="${PWD}/apps/backend"
PHASE=${1:-"all"}
DRY_RUN=false
INTERACTIVE=false
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="onboarding_report_${TIMESTAMP}.txt"
BACKUP_DIR="backup_onboarding_${TIMESTAMP}"

PHASE_1_MODULES=("monitoring")
PHASE_2_MODULES=("common")
PHASE_3_MODULES=("auth")

# ============================================================================
# CORES
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
RESET='\033[0m'

# ============================================================================
# HELPERS
# ============================================================================

print_banner() {
    echo -e "${MAGENTA}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║          🚀 SILA System - Onboarding & Migração                ║"
    echo "║  Orquestra análise → classificação → migração → validação      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${RESET}"
}

print_header() {
    echo -e "\n${BOLD}${CYAN}══════════════════════════════════════════${RESET}"
    echo -e "${BOLD}${CYAN}$1${RESET}"
    echo -e "${BOLD}${CYAN}══════════════════════════════════════════${RESET}\n"
}

print_step() {
    echo -e "${BLUE}→${RESET} $1"
}

print_success() {
    echo -e "${GREEN}✓${RESET} $1"
}

print_error() {
    echo -e "${RED}✗${RESET} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${RESET} $1"
}

ask_confirm() {
    local prompt=$1
    echo -n -e "${YELLOW}${prompt} (s/n)? ${RESET}"
    read -r response
    [[ "$response" =~ ^[sS]$ ]]
}

# ============================================================================
# ETAPA 0: Preparação
# ============================================================================

prepare() {
    print_header "📋 ETAPA 0: Preparação"

    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 não encontrado"
        return 1
    fi
    print_success "Python3 encontrado"

    # Verificar git
    if ! command -v git &> /dev/null; then
        print_error "Git não encontrado"
        return 1
    fi
    print_success "Git encontrado"

    # Verificar status git
    if [ ! -z "$(git status -s)" ]; then
        print_warning "Repositório com mudanças não commitadas"
        if ask_confirm "Deseja commitá-las antes de continuar?"; then
            git add -A
            git commit -m "chore: checkpoint antes de onboarding"
            print_success "Mudanças commitadas"
        fi
    fi

    # Criar backup
    print_step "Criando backup..."
    mkdir -p "$BACKUP_DIR"
    cp -r "${BACKEND_PATH}/modules" "$BACKUP_DIR/" 2>/dev/null || true
    cp -r "${BACKEND_PATH}/core" "$BACKUP_DIR/" 2>/dev/null || true
    print_success "Backup criado em: $BACKUP_DIR"

    # Inicializar relatório
    {
        echo "═══════════════════════════════════════════════════════════════"
        echo "ONBOARDING & MIGRAÇÃO - RELATÓRIO COMPLETO"
        echo "═══════════════════════════════════════════════════════════════"
        echo "Data/Hora: $(date)"
        echo "Fase: $PHASE"
        echo "Modo: $([ "$DRY_RUN" = true ] && echo "DRY-RUN" || echo "REAL")"
        echo ""
    } > "$REPORT_FILE"

    print_success "Preparação concluída"
}

# ============================================================================
# ETAPA 1: Análise
# ============================================================================

analyze() {
    print_header "🔍 ETAPA 1: Análise da Estrutura"

    print_step "Executando migration_analyzer.py..."

    if [ ! -f "migration_analyzer.py" ]; then
        print_error "migration_analyzer.py não encontrado"
        return 1
    fi

    if python3 migration_analyzer.py --save migration_analysis_report.json >> "$REPORT_FILE" 2>&1; then
        print_success "Análise completa"
        print_info "  Dados salvos em: migration_analysis_report.json"
    else
        print_error "Erro ao analisar"
        return 1
    fi
}

print_info() {
    echo -e "${BLUE}ℹ${RESET} $1"
}

# ============================================================================
# ETAPA 2: Classificação
# ============================================================================

classify() {
    print_header "🎯 ETAPA 2: Classificação de Módulos"

    print_step "Executando module_classifier.py..."

    if [ ! -f "module_classifier.py" ]; then
        print_error "module_classifier.py não encontrado"
        return 1
    fi

    if python3 module_classifier.py --export module_classifications.json >> "$REPORT_FILE" 2>&1; then
        print_success "Classificação completa"
        print_info "  Dados salvos em: module_classifications.json"
    else
        print_error "Erro ao classificar"
        return 1
    fi
}

# ============================================================================
# ETAPA 3: Validação Pré-Migração
# ============================================================================

validate_pre() {
    print_header "✅ ETAPA 3: Validação Pré-Migração"

    print_step "Verificando testes antes..."

    if command -v pytest &> /dev/null; then
        if pytest tests/ -q --tb=no 2>&1 | tee -a "$REPORT_FILE"; then
            print_success "Testes OK antes da migração"
        else
            print_warning "Alguns testes falhando (continuando...)"
        fi
    else
        print_warning "pytest não disponível"
    fi
}

# ============================================================================
# ETAPA 4: Migração (por fase)
# ============================================================================

migrate_phase() {
    local phase=$1
    local modules=("$@")
    modules=("${modules[@]:1}")  # Remove primeiro argumento (phase)

    print_header "🔄 ETAPA 4.${phase}: Migração - Fase ${phase}"

    for module in "${modules[@]}"; do
        local from_pattern="modules.${module}"
        local to_pattern=""

        # Determinar padrão de destino
        case $module in
            monitoring) to_pattern="core.monitoring" ;;
            common) to_pattern="core.utils.common" ;;
            auth) to_pattern="core.auth" ;;
            *) to_pattern="core.${module}" ;;
        esac

        print_step "Migrando: ${from_pattern} → ${to_pattern}"

        # DRY RUN
        print_info "  [1/2] Executando dry-run..."
        if ! python3 update_imports.py \
            --from "$from_pattern" \
            --to "$to_pattern" \
            --dry-run \
            --recursive >> "$REPORT_FILE" 2>&1; then
            print_error "Dry-run falhou"
            return 1
        fi
        print_success "  Dry-run OK"

        # REAL RUN
        if [ "$DRY_RUN" != true ]; then
            print_info "  [2/2] Executando migração real..."
            if ! python3 update_imports.py \
                --from "$from_pattern" \
                --to "$to_pattern" \
                --backup \
                --recursive >> "$REPORT_FILE" 2>&1; then
                print_error "Migração falhou"
                return 1
            fi
            print_success "  Migração OK"
        else
            print_info "  [2/2] Pulado (DRY-RUN)"
        fi
    done
}

# ============================================================================
# ETAPA 5: Validação Pós-Migração
# ============================================================================

validate_post() {
    print_header "✅ ETAPA 5: Validação Pós-Migração"

    print_step "Executando validações..."

    if [ ! -f "validate_migration.py" ]; then
        print_error "validate_migration.py não encontrado"
        return 1
    fi

    python3 validate_migration.py --check-all >> "$REPORT_FILE" 2>&1 || true

    # Verificar imports
    print_step "Verificando imports após migração..."
    if python3 validate_migration.py --check-imports >> "$REPORT_FILE" 2>&1; then
        print_success "Imports validados"
    else
        print_warning "Problemas com imports (revisar)"
    fi

    # Testes
    print_step "Executando testes pós-migração..."
    if command -v pytest &> /dev/null; then
        if pytest tests/ -q --tb=no 2>&1 | tee -a "$REPORT_FILE"; then
            print_success "Testes OK após migração"
        else
            print_warning "Alguns testes falhando"
        fi
    fi
}

# ============================================================================
# ETAPA 6: Verificação de Estrutura
# ============================================================================

check_structure() {
    print_header "🛡️  ETAPA 6: Verificação de Estrutura"

    if [ -f "structure-guard.sh" ]; then
        print_step "Executando structure-guard..."
        bash structure-guard.sh --check >> "$REPORT_FILE" 2>&1 || true
        print_success "Verificação concluída"
    else
        print_warning "structure-guard.sh não encontrado"
    fi
}

# ============================================================================
# ETAPA 7: Monitoramento
# ============================================================================

monitor() {
    print_header "👁️  ETAPA 7: Monitoramento"

    if [ -f "monitor-migration.sh" ]; then
        print_step "Executando monitor-migration..."
        bash monitor-migration.sh --report >> "$REPORT_FILE" 2>&1 || true
        print_success "Monitoramento concluído"
    else
        print_warning "monitor-migration.sh não encontrado"
    fi
}

# ============================================================================
# ETAPA 8: Relatório Final
# ============================================================================

finalize() {
    print_header "📄 ETAPA 8: Relatório Final"

    {
        echo ""
        echo "═══════════════════════════════════════════════════════════════"
        echo "RESULTADO FINAL"
        echo "═══════════════════════════════════════════════════════════════"
        echo ""
        echo "Status: $([ "$DRY_RUN" = true ] && echo "DRY-RUN (SEM MODIFICAÇÕES)" || echo "MIGRAÇÃO EXECUTADA")"
        echo "Data: $(date)"
        echo ""
        echo "Próximos passos:"
        echo "  1. Revisar relatório: $REPORT_FILE"
        echo "  2. Fazer code review"
        echo "  3. Merge para main"
        echo "  4. Deploy staging"
        echo ""
        echo "Backup disponível em: $BACKUP_DIR"
        echo ""
    } >> "$REPORT_FILE"

    print_success "Relatório salvo: $REPORT_FILE"

    # Exibir resumo
    echo ""
    echo -e "${BOLD}${GREEN}══════════════════════════════════════════${RESET}"
    tail -15 "$REPORT_FILE"
    echo -e "${BOLD}${GREEN}══════════════════════════════════════════${RESET}"
}

# ============================================================================
# MENU INTERATIVO
# ============================================================================

interactive_menu() {
    while true; do
        clear
        print_banner
        echo ""
        echo "O que deseja fazer?"
        echo ""
        echo "  1) Fase 1: Migração de monitoring (baixo risco)"
        echo "  2) Fase 2: Migração de common (baixo risco)"
        echo "  3) Fase 3: Migração de auth (alto risco)"
        echo "  4) Todas as fases (análise + migração + validação)"
        echo "  5) Apenas análise (sem migração)"
        echo "  6) Sair"
        echo ""
        echo -n "Escolha uma opção (1-6): "
        read -r choice

        case $choice in
            1)
                PHASE=1
                break
                ;;
            2)
                PHASE=2
                break
                ;;
            3)
                PHASE=3
                break
                ;;
            4)
                PHASE=all
                break
                ;;
            5)
                PHASE=analyze_only
                break
                ;;
            6)
                print_info "Saindo..."
                exit 0
                ;;
            *)
                print_error "Opção inválida"
                ;;
        esac
    done

    # Perguntar sobre dry-run
    if ask_confirm "Executar em modo DRY-RUN (sem modificar arquivos)?"; then
        DRY_RUN=true
        print_info "Modo DRY-RUN ativado"
    fi
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Parse argumentos
    while [[ $# -gt 0 ]]; do
        case $1 in
            --phase)
                PHASE="${2}"
                shift 2
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --interactive)
                INTERACTIVE=true
                shift
                ;;
            --help)
                echo "Uso: $0 [opções]"
                echo "  --phase N           Fase específica (1, 2, 3, all)"
                echo "  --dry-run           Não modificar arquivos"
                echo "  --interactive       Menu interativo"
                exit 0
                ;;
            *)
                shift
                ;;
        esac
    done

    print_banner

    # Menu interativo
    if [ "$INTERACTIVE" = true ]; then
        interactive_menu
    fi

    # Preparação
    prepare || exit 1

    # Executar baseado em PHASE
    case $PHASE in
        analyze_only)
            analyze || exit 1
            classify || exit 1
            validate_pre || true
            ;;
        1)
            analyze || exit 1
            classify || exit 1
            validate_pre || true
            migrate_phase 1 "${PHASE_1_MODULES[@]}" || exit 1
            validate_post || true
            check_structure || true
            monitor || true
            ;;
        2)
            analyze || exit 1
            classify || exit 1
            validate_pre || true
            migrate_phase 2 "${PHASE_2_MODULES[@]}" || exit 1
            validate_post || true
            check_structure || true
            monitor || true
            ;;
        3)
            print_warning "Fase 3 é alto risco (140 arquivos afetados)"
            if ! ask_confirm "Deseja continuar?"; then
                print_info "Cancelado"
                exit 0
            fi
            analyze || exit 1
            classify || exit 1
            validate_pre || true
            migrate_phase 3 "${PHASE_3_MODULES[@]}" || exit 1
            validate_post || true
            check_structure || true
            monitor || true
            ;;
        all)
            analyze || exit 1
            classify || exit 1
            validate_pre || true
            migrate_phase 1 "${PHASE_1_MODULES[@]}" || exit 1
            validate_post || true
            migrate_phase 2 "${PHASE_2_MODULES[@]}" || exit 1
            validate_post || true
            migrate_phase 3 "${PHASE_3_MODULES[@]}" || exit 1
            validate_post || true
            check_structure || true
            monitor || true
            ;;
        *)
            print_error "Fase inválida: $PHASE"
            exit 1
            ;;
    esac

    # Finalização
    finalize

    print_header "✅ ONBOARDING COMPLETO"
    echo -e "${GREEN}${BOLD}Sucesso! Verifique o relatório:${RESET}"
    echo "  cat $REPORT_FILE"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
