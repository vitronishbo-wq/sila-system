#!/bin/bash
################################################################################
# 🛡️  SILA System - Structure Guard
# Protege regras arquiteturais pós-migração
# - modules/ = negócio (citizenship, justice, finance, etc)
# - core/ = técnico (auth, monitoring, logging, database, etc)
# - Valida imports cross-layer
#
# Uso:
#   ./structure-guard.sh --check          # Validar regras
#   ./structure-guard.sh --fix            # Corrigir automaticamente
#   ./structure-guard.sh --report         # Gerar relatório
#   ./structure-guard.sh --strict         # Modo rigoroso (pará na primeira violação)
################################################################################

set -euo pipefail

# ============================================================================
# CORES
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

BACKEND_PATH="${PWD}/apps/backend"
MODULES_PATH="${BACKEND_PATH}/modules"
CORE_PATH="${BACKEND_PATH}/core"
VIOLATIONS=0
FIX_MODE=false
STRICT_MODE=false
REPORT_MODE=false

# ============================================================================
# REGRAS DE ARQUITETURA
# ============================================================================

# Domínios de negócio (devem estar em modules/)
BUSINESS_DOMAINS=(
    "citizenship" "justice" "finance" "governance" "health"
    "education" "location" "address" "payment" "notifications"
    "documents" "analytics" "dashboard" "complaints" "commercial"
    "appointments" "training" "registry" "statistics" "identity"
    "service_hub" "social" "journeys" "reports" "urbanism"
)

# Componentes técnicos (devem estar em core/)
TECHNICAL_COMPONENTS=(
    "auth" "authentication"
    "monitoring" "observability"
    "logging" "logger" "logs"
    "database" "db" "repositories"
    "exceptions" "error" "errors"
    "security" "permissions"
    "middleware" "decorators"
    "schemas" "validators"
    "utils" "helpers" "constants"
)

# ============================================================================
# HELPERS
# ============================================================================

print_header() {
    echo -e "\n${BOLD}${CYAN}════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}${CYAN}$1${RESET}"
    echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${RESET}\n"
}

print_violation() {
    echo -e "${RED}✗${RESET} $1"
    ((VIOLATIONS++))
}

print_success() {
    echo -e "${GREEN}✓${RESET} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${RESET} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${RESET} $1"
}

# ============================================================================
# CHECK 1: Business Domains em modules/
# ============================================================================

check_business_domains() {
    print_header "🎯 Verificando Domínios de Negócio"

    local issues=0

    for domain in "${BUSINESS_DOMAINS[@]}"; do
        # Verificar se existe em modules/
        if [ -d "${MODULES_PATH}/${domain}" ]; then
            local files=$(find "${MODULES_PATH}/${domain}" -name "*.py" | wc -l)
            print_success "modules/${domain}/ encontrado ($files arquivos)"
        else
            # Verificar se errou e foi para core/
            if [ -d "${CORE_PATH}/${domain}" ]; then
                print_violation "modules/${domain}/ NÃO encontrado, mas core/${domain}/ EXISTS!"
                print_warning "  → Mover de volta: mv ${CORE_PATH}/${domain} ${MODULES_PATH}/"
                ((issues++))
            fi
        fi
    done

    return $issues
}

# ============================================================================
# CHECK 2: Technical Components em core/
# ============================================================================

check_technical_components() {
    print_header "🔧 Verificando Componentes Técnicos"

    local issues=0

    for component in "${TECHNICAL_COMPONENTS[@]}"; do
        # Verificar se existe em core/
        if [ -d "${CORE_PATH}/${component}" ] || [ -f "${CORE_PATH}/${component}.py" ]; then
            local files=$(find "${CORE_PATH}/${component}" -name "*.py" 2>/dev/null | wc -l || echo 1)
            print_success "core/${component}/ encontrado ($files arquivos)"
        else
            # Verificar se errou e foi para modules/
            if [ -d "${MODULES_PATH}/${component}" ]; then
                print_violation "core/${component}/ NÃO encontrado, mas modules/${component}/ EXISTS!"
                print_warning "  → Mover: mv ${MODULES_PATH}/${component} ${CORE_PATH}/"
                ((issues++))
            fi
        fi
    done

    return $issues
}

# ============================================================================
# CHECK 3: Imports Válidos
# ============================================================================

check_imports() {
    print_header "🔗 Validando Imports Cross-Layer"

    local issues=0

    print_info "Regra 1: Negócio CAN importar de técnico"
    print_info "  Válido:   from core.auth import..."
    print_info "  Inválido: from modules.auth import..."

    local bad_imports=$(grep -r "from modules\\.auth" "${MODULES_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)
    if [ "$bad_imports" -gt 0 ]; then
        print_violation "Encontrados $bad_imports imports inválidos de modules.auth"
        ((issues++))
    else
        print_success "Nenhum import inválido de modules.auth"
    fi

    print_info ""
    print_info "Regra 2: Técnico NÃO deve importar de negócio"
    print_info "  Inválido: from modules.citizenship import..."

    local bad_tech_imports=$(grep -r "from modules\\." "${CORE_PATH}" --include="*.py" 2>/dev/null | grep -v "from modules\\.common" | wc -l || echo 0)
    if [ "$bad_tech_imports" -gt 0 ]; then
        print_violation "Encontrados $bad_tech_imports imports de core/ para modules/"
        grep -r "from modules\\." "${CORE_PATH}" --include="*.py" 2>/dev/null | head -3
        ((issues++))
    else
        print_success "core/ não importa de modules/"
    fi

    return $issues
}

# ============================================================================
# CHECK 4: Arquivos Orfãos
# ============================================================================

check_orphaned_files() {
    print_header "👻 Procurando Arquivos Orfãos"

    local orphaned=0

    # Procurar .py soltos em backend/ (não em modules/ ou core/ ou app/)
    print_info "Verificando arquivos .py diretamente em apps/backend/..."

    local stray_files=$(find "${BACKEND_PATH}" -maxdepth 1 -name "*.py" -type f 2>/dev/null | wc -l)
    if [ "$stray_files" -gt 0 ]; then
        print_warning "Encontrados $stray_files arquivos .py soltos em backend/"
        find "${BACKEND_PATH}" -maxdepth 1 -name "*.py" -type f 2>/dev/null | while read f; do
            print_warning "  → $f (deve estar em core/ ou modules/)"
        done
        ((orphaned++))
    else
        print_success "Nenhum arquivo orfão"
    fi

    return $orphaned
}

# ============================================================================
# CHECK 5: Nomeação Consistente
# ============================================================================

check_naming() {
    print_header "📝 Verificando Nomeação Consistente"

    local issues=0

    # Padrão de negócio: Deve ter models.py, schemas.py, services.py
    print_info "Estrutura esperada em domínios de negócio:"

    for domain in "${BUSINESS_DOMAINS[@]}"; do
        if [ -d "${MODULES_PATH}/${domain}" ]; then
            local has_models=$([ -f "${MODULES_PATH}/${domain}/models.py" ] && echo "✓" || echo "✗")
            local has_routes=$([ -f "${MODULES_PATH}/${domain}/routes.py" ] && echo "✓" || echo "✗")
            local has_services=$([ -f "${MODULES_PATH}/${domain}/services.py" ] && echo "✓" || echo "✗")

            echo "  ${domain}: models($has_models) routes($has_routes) services($has_services)"
        fi
    done

    return 0
}

# ============================================================================
# RELATÓRIO DETALHADO
# ============================================================================

generate_report() {
    print_header "📄 Gerando Relatório Detalhado"

    local report_file="structure-guard-report-$(date +%Y%m%d_%H%M%S).txt"

    {
        echo "Structure Guard Report"
        echo "======================="
        echo "Data: $(date)"
        echo ""
        echo "SUMÁRIO:"
        echo "--------"
        echo "Violações encontradas: $VIOLATIONS"
        echo ""

        echo "DOMÍNIOS DE NEGÓCIO (modules/):"
        for domain in "${BUSINESS_DOMAINS[@]}"; do
            if [ -d "${MODULES_PATH}/${domain}" ]; then
                echo "  ✓ $domain"
            else
                echo "  ✗ $domain (FALTANDO)"
            fi
        done

        echo ""
        echo "COMPONENTES TÉCNICOS (core/):"
        for component in "${TECHNICAL_COMPONENTS[@]}"; do
            if [ -d "${CORE_PATH}/${component}" ] || [ -f "${CORE_PATH}/${component}.py" ]; then
                echo "  ✓ $component"
            else
                echo "  ✗ $component (FALTANDO)"
            fi
        done

        echo ""
        echo "IMPORTS CRÍTICOS:"
        echo "  Imports de modules.auth em negócio: $(grep -r "from modules\\.auth" "${MODULES_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)"
        echo "  Imports de modules em core: $(grep -r "from modules\\." "${CORE_PATH}" --include="*.py" 2>/dev/null | wc -l || echo 0)"

    } > "$report_file"

    print_success "Relatório salvo: $report_file"
    cat "$report_file"
}

# ============================================================================
# AUTO-FIX
# ============================================================================

auto_fix() {
    print_header "🔧 Modo Auto-Fix"

    print_warning "CUIDADO: Isto pode mover arquivos!"
    echo -n "Confirmar? (s/n): "
    read -r confirm

    if [ "$confirm" != "s" ]; then
        print_info "Cancelado"
        return 0
    fi

    # Procurar arquivos técnicos em modules/ e mover para core/
    print_info "Movendo componentes técnicos para core/..."

    for component in auth monitoring logging database; do
        if [ -d "${MODULES_PATH}/${component}" ] && [ ! -d "${CORE_PATH}/${component}" ]; then
            print_info "Movendo: ${MODULES_PATH}/${component} → ${CORE_PATH}/"
            mkdir -p "${CORE_PATH}"
            mv "${MODULES_PATH}/${component}" "${CORE_PATH}/"
        fi
    done

    print_success "Auto-fix completo"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --check)
                shift
                ;;
            --fix)
                FIX_MODE=true
                shift
                ;;
            --report)
                REPORT_MODE=true
                shift
                ;;
            --strict)
                STRICT_MODE=true
                shift
                ;;
            --help)
                echo "Uso: $0 [opções]"
                echo "  --check      Validar regras"
                echo "  --fix        Corrigir automaticamente"
                echo "  --report     Gerar relatório"
                echo "  --strict     Parar na primeira violação"
                exit 0
                ;;
            *)
                shift
                ;;
        esac
    done

    print_header "🛡️  STRUCTURE GUARD - Proteção de Arquitetura"

    # Executar checks
    check_business_domains || true
    check_technical_components || true
    check_imports || true
    check_orphaned_files || true
    check_naming || true

    # Modo strict: parar se violações
    if [ "$STRICT_MODE" = true ] && [ $VIOLATIONS -gt 0 ]; then
        print_header "❌ STRICT MODE: Violações encontradas!"
        exit 1
    fi

    # Auto-fix
    if [ "$FIX_MODE" = true ]; then
        auto_fix
    fi

    # Relatório
    if [ "$REPORT_MODE" = true ]; then
        generate_report
    fi

    # Resumo
    print_header "📋 RESUMO"
    if [ $VIOLATIONS -eq 0 ]; then
        echo -e "${GREEN}${BOLD}✅ Arquitetura OK - Nenhuma violação!${RESET}"
        return 0
    else
        echo -e "${YELLOW}${BOLD}⚠️  $VIOLATIONS VIOLAÇÕES ENCONTRADAS${RESET}"
        return 1
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
