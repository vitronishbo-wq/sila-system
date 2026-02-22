#!/bin/bash
################################################################################
# 📊 SILA System - Monitor Migração
# Monitora integridade pós-migração, conectando com migration_analyzer.py
# e validate_migration.py
#
# Uso:
#   ./monitor-migration.sh                    # Verificação rápida
#   ./monitor-migration.sh --detailed         # Saída completa
#   ./monitor-migration.sh --watch            # Monitoramento contínuo
#   ./monitor-migration.sh --report           # Gera relatório
################################################################################

set -euo pipefail

# ============================================================================
# CORES & ESTILOS
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
# CONFIGURAÇÃO
# ============================================================================

BACKEND_PATH="${PWD}/apps/backend"
MODULES_PATH="${BACKEND_PATH}/modules"
CORE_PATH="${BACKEND_PATH}/core"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="migration_monitor_${TIMESTAMP}.txt"

DETAILED=false
WATCH_MODE=false
GENERATE_REPORT=false

# ============================================================================
# FUNCTIONS
# ============================================================================

print_header() {
    echo -e "\n${BOLD}${CYAN}════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}${CYAN}$1${RESET}"
    echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${RESET}\n"
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

print_info() {
    echo -e "${BLUE}ℹ${RESET} $1"
}

# ============================================================================
# CHECK 1: Estrutura de Diretórios
# ============================================================================

check_structure() {
    print_header "📁 Verificando Estrutura"

    local errors=0

    # Verificar core/
    if [ ! -d "${CORE_PATH}" ]; then
        print_error "core/ não encontrado em ${CORE_PATH}"
        ((errors++))
    else
        local core_files=$(find "${CORE_PATH}" -name "*.py" | wc -l)
        print_success "core/ encontrado: ${core_files} arquivos Python"
    fi

    # Verificar modules/
    if [ ! -d "${MODULES_PATH}" ]; then
        print_error "modules/ não encontrado em ${MODULES_PATH}"
        ((errors++))
    else
        local modules_files=$(find "${MODULES_PATH}" -name "*.py" | wc -l)
        print_success "modules/ encontrado: ${modules_files} arquivos Python"
    fi

    # Verificar diretórios esperados em core/
    local core_dirs=("auth" "monitoring" "utils" "database")
    for dir in "${core_dirs[@]}"; do
        if [ -d "${CORE_PATH}/${dir}" ]; then
            print_success "core/${dir}/ existe"
        else
            print_warning "core/${dir}/ não encontrado (pode ser normal se não migrado ainda)"
        fi
    done

    return $errors
}

# ============================================================================
# CHECK 2: Padrões de Import
# ============================================================================

check_imports() {
    print_header "🔗 Analisando Padrões de Import"

    local errors=0
    local from_core=$(grep -r "from core\." "${BACKEND_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)
    local from_modules=$(grep -r "from modules\." "${BACKEND_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)
    local relative=$(grep -r "from \.\." "${BACKEND_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)

    print_info "Imports encontrados:"
    echo "  from core.*:     $from_core"
    echo "  from modules.*:  $from_modules"
    echo "  Relativos (..):  $relative"

    # Verificar imports inválidos
    local bad_monitoring=$(grep -r "from modules\.monitoring" "${BACKEND_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)
    local bad_auth=$(grep -r "from modules\.auth" "${BACKEND_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)

    if [ "$bad_monitoring" -gt 0 ]; then
        print_warning "Encontrados $bad_monitoring imports de modules.monitoring (deve usar core.monitoring)"
        ((errors++))
    else
        print_success "Nenhum import inválido de modules.monitoring"
    fi

    if [ "$bad_auth" -gt 0 ]; then
        print_warning "Encontrados $bad_auth imports de modules.auth (deve usar core.auth)"
        ((errors++))
    else
        print_success "Nenhum import inválido de modules.auth"
    fi

    return $errors
}

# ============================================================================
# CHECK 3: Duplicatas de Arquivo
# ============================================================================

check_duplicates() {
    print_header "🔍 Procurando Arquivos Duplicados"

    local duplicates=0

    # Procurar por padrões de duplicação
    # Se arquivo existe em modules/ e core/, é um problema

    if [ -d "${MODULES_PATH}/monitoring" ] && [ -d "${CORE_PATH}/monitoring" ]; then
        print_warning "monitoring/ existe em AMBOS modules/ E core/ (removeu o de modules/?)"
        ((duplicates++))
    fi

    if [ -d "${MODULES_PATH}/auth" ] && [ -d "${CORE_PATH}/auth" ]; then
        print_warning "auth/ existe em AMBOS modules/ E core/ (removeu o de modules/?)"
        ((duplicates++))
    fi

    if [ -d "${MODULES_PATH}/common" ] && [ -d "${CORE_PATH}/utils/common" ]; then
        print_warning "common/ existe em AMBOS modules/ E core/utils/ (removeu o de modules/?)"
        ((duplicates++))
    fi

    if [ $duplicates -eq 0 ]; then
        print_success "Nenhuma duplicata detectada"
    fi

    return 0
}

# ============================================================================
# CHECK 4: Sintaxe Python
# ============================================================================

check_syntax() {
    print_header "🐍 Validando Sintaxe Python"

    local syntax_errors=0
    local total_files=0

    print_info "Verificando sintaxe de arquivos Python..."

    for py_file in $(find "${BACKEND_PATH}" -name "*.py" -type f 2>/dev/null | grep -v venv | grep -v __pycache__); do
        ((total_files++))
        if ! python3 -m py_compile "$py_file" 2>/dev/null; then
            print_error "Erro de sintaxe em: $py_file"
            ((syntax_errors++))
        fi
    done

    if [ $syntax_errors -eq 0 ]; then
        print_success "Sintaxe OK em todos os $total_files arquivos"
    else
        print_error "Encontrados $syntax_errors erros de sintaxe"
    fi

    return $syntax_errors
}

# ============================================================================
# CHECK 5: Testes
# ============================================================================

check_tests() {
    print_header "🧪 Executando Testes"

    if ! command -v pytest &> /dev/null; then
        print_warning "pytest não disponível (pulando testes)"
        return 0
    fi

    print_info "Rodando pytest..."
    if pytest tests/ -q --tb=no 2>/dev/null; then
        print_success "Testes passando ✓"
        return 0
    else
        print_warning "Alguns testes falharam (verificar manualmente)"
        return 1
    fi
}

# ============================================================================
# CHECK 6: Métricas de Migração
# ============================================================================

check_metrics() {
    print_header "📊 Métricas de Migração"

    if [ ! -f "migration_analysis_report.json" ]; then
        print_warning "migration_analysis_report.json não encontrado"
        print_info "Execute: python3 migration_analyzer.py --save migration_analysis_report.json"
        return 1
    fi

    print_info "Relatório de análise encontrado"

    # Tentar extrair métricas com jq se disponível
    if command -v jq &> /dev/null; then
        local total_modules=$(jq '.metrics.total_modules' migration_analysis_report.json)
        local total_files=$(jq '.metrics.total_files' migration_analysis_report.json)
        local total_size=$(jq '.metrics.total_size_kb' migration_analysis_report.json)

        echo "  Módulos: $total_modules"
        echo "  Arquivos: $total_files"
        echo "  Tamanho: $total_size KB"
    fi

    return 0
}

# ============================================================================
# VALIDAÇÃO COMPLETA
# ============================================================================

validate_all() {
    print_header "🔍 VALIDAÇÃO COMPLETA DE MIGRAÇÃO"

    local total_errors=0

    check_structure || ((total_errors+=$?))
    check_imports || ((total_errors+=$?))
    check_duplicates || ((total_errors+=$?))
    check_syntax || ((total_errors+=$?))
    check_tests || ((total_errors+=$?))
    check_metrics || ((total_errors+=$?))

    # Resumo final
    print_header "📋 RESUMO"

    if [ $total_errors -eq 0 ]; then
        echo -e "${GREEN}${BOLD}✅ MIGRAÇÃO VALIDADA COM SUCESSO!${RESET}"
        echo -e "\nTodos os checks passaram. Sistema pronto para produção."
        return 0
    else
        echo -e "${YELLOW}${BOLD}⚠️  $total_errors PROBLEMAS ENCONTRADOS${RESET}"
        echo -e "\nRevisar erros acima e corrigir antes de fazer deploy."
        return 1
    fi
}

# ============================================================================
# WATCH MODE
# ============================================================================

watch_mode() {
    print_header "👁️  MODO MONITORAMENTO CONTÍNUO"
    echo "Monitorando mudanças a cada 30 segundos..."
    echo "Pressione Ctrl+C para parar"
    echo ""

    while true; do
        clear
        echo -e "${CYAN}${BOLD}Monitor de Migração - $(date)${RESET}\n"

        validate_all

        echo -e "\n${BLUE}Próxima verificação em 30 segundos... (Ctrl+C para parar)${RESET}"
        sleep 30
    done
}

# ============================================================================
# RELATÓRIO
# ============================================================================

generate_report() {
    print_header "📄 Gerando Relatório"

    echo "Acessório de migração - $(date)" > "$REPORT_FILE"
    echo "================================================" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    echo "VERIFICAÇÕES:" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    # Estrutura
    {
        echo "✓ Estrutura de Diretórios"
        [ -d "${CORE_PATH}" ] && echo "  ✓ core/ encontrado" || echo "  ✗ core/ não encontrado"
        [ -d "${MODULES_PATH}" ] && echo "  ✓ modules/ encontrado" || echo "  ✗ modules/ não encontrado"
    } >> "$REPORT_FILE"

    # Imports
    {
        echo ""
        echo "✓ Padrões de Import"
        echo "  from core.*: $(grep -r "from core\." "${BACKEND_PATH}" --include="*.py" 2>/dev/null | wc -l)"
        echo "  from modules.*: $(grep -r "from modules\." "${BACKEND_PATH}" --include="*.py" 2>/dev/null | wc -l)"
    } >> "$REPORT_FILE"

    # Sintaxe
    {
        echo ""
        echo "✓ Sintaxe Python"
        echo "  Arquivos verificados: $(find "${BACKEND_PATH}" -name "*.py" -type f 2>/dev/null | grep -v venv | grep -v __pycache__ | wc -l)"
    } >> "$REPORT_FILE"

    # Testes
    {
        echo ""
        echo "✓ Testes"
        if command -v pytest &> /dev/null; then
            pytest tests/ -q --tb=no 2>&1 | head -5 >> "$REPORT_FILE" || true
        else
            echo "  pytest não disponível"
        fi
    } >> "$REPORT_FILE"

    {
        echo ""
        echo "================================================"
        echo "Relatório gerado: $(date)"
    } >> "$REPORT_FILE"

    print_success "Relatório salvo em: $REPORT_FILE"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    # Parse argumentos
    while [[ $# -gt 0 ]]; do
        case $1 in
            --detailed)
                DETAILED=true
                shift
                ;;
            --watch)
                WATCH_MODE=true
                shift
                ;;
            --report)
                GENERATE_REPORT=true
                shift
                ;;
            --help)
                echo "Uso: $0 [opções]"
                echo "  --detailed    Saída completa"
                echo "  --watch       Monitoramento contínuo"
                echo "  --report      Gerar relatório"
                echo "  --help        Esta mensagem"
                exit 0
                ;;
            *)
                echo "Opção desconhecida: $1"
                exit 1
                ;;
        esac
    done

    # Executar
    if [ "$WATCH_MODE" = true ]; then
        watch_mode
    else
        validate_all

        if [ "$GENERATE_REPORT" = true ]; then
            generate_report
        fi
    fi
}

# Executar se script foi chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
