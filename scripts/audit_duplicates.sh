#!/bin/bash

################################################################################
# AUDITORIA DE SCRIPTS - Detecção de Funções e Regras Duplicadas
# Objetivo: Identificar duplicações que impactam desempenho do projeto
################################################################################

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_FILE="$SCRIPTS_DIR/audit_duplicates_$(date +%Y%m%d_%H%M%S).txt"

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

print_header() {
    echo -e "\n${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}$1${NC}"
    echo -e "${BOLD}${CYAN}════════════════════════════════════════════════════════════${NC}\n"
}

log_result() {
    echo -e "$1" | tee -a "$REPORT_FILE"
}

# ============================================================================
# AUDITORIA 1: Funções de Logging Duplicadas
# ============================================================================

audit_logging_functions() {
    print_header "[1/6] AUDITORIA: Funções de Logging Duplicadas"

    log_result "🔍 Procurando funções de logging (log, success, error, warn, info)...\n"

    local files_with_logging=()
    local count=0

    while IFS= read -r file; do
        if grep -qE "^(log|success|error|warn|info)\(\)" "$file" 2>/dev/null; then
            files_with_logging+=("$file")
            ((count++))
        fi
    done < <(find "$SCRIPTS_DIR" -name "*.sh" -type f 2>/dev/null)

    if [ $count -gt 0 ]; then
        log_result "⚠️  DUPLICAÇÃO ENCONTRADA: $count scripts com funções de logging duplicadas\n"
        for file in "${files_with_logging[@]}"; do
            log_result "   📄 $file"
        done
        log_result "\n🔴 IMPACTO: Cada script redefine as mesmas funções, aumentando tamanho e tempo de carregamento"
        log_result "💡 SOLUÇÃO: Criar arquivo comum 'scripts/lib/logging.sh' e fazer source\n"
    else
        log_result "✅ Nenhuma duplicação de logging encontrada\n"
    fi
}

# ============================================================================
# AUDITORIA 2: Definições de Cores Duplicadas
# ============================================================================

audit_color_definitions() {
    print_header "[2/6] AUDITORIA: Definições de Cores Duplicadas"

    log_result "🔍 Procurando definições de cores (RED, GREEN, BLUE, etc)...\n"

    local files_with_colors=()
    local count=0

    while IFS= read -r file; do
        if grep -q "RED=.*033" "$file" 2>/dev/null; then
            files_with_colors+=("$file")
            ((count++))
        fi
    done < <(find "$SCRIPTS_DIR" -name "*.sh" -type f)

    if [ $count -gt 0 ]; then
        log_result "⚠️  DUPLICAÇÃO ENCONTRADA: $count scripts com definições de cores duplicadas\n"
        for file in "${files_with_colors[@]}"; do
            log_result "   📄 $file"
        done
        log_result "\n🔴 IMPACTO: Cada script redefine as mesmas cores, aumentando tamanho dos arquivos"
        log_result "💡 SOLUÇÃO: Centralizar em 'scripts/lib/colors.sh'\n"
    else
        log_result "✅ Nenhuma duplicação de cores encontrada\n"
    fi
}

# ============================================================================
# AUDITORIA 3: Scripts com Nomes Similares
# ============================================================================

audit_similar_names() {
    print_header "[3/6] AUDITORIA: Scripts com Nomes Similares (Possível Duplicação)"

    log_result "🔍 Procurando scripts com nomes similares...\n"

    # Procurar por padrões similares
    local duplicates=(
        "sila_start.sh:start_sila.sh"
        "monitor-migration.sh:nginx_monitor.sh"
        "cleanup_all_backups.sh:cleanup_obsolete.sh:cleanup_project.sh"
        "repair_all_runner.sh:repair_all_simple.sh"
        "project_analyzer.sh:advanced_project_analyzer.sh"
    )

    local found_any=false

    for pattern in "${duplicates[@]}"; do
        IFS=':' read -ra scripts <<< "$pattern"
        local existing_count=0

        for script in "${scripts[@]}"; do
            if find "$SCRIPTS_DIR" -name "$script" -type f | grep -q .; then
                ((existing_count++))
            fi
        done

        if [ $existing_count -gt 1 ]; then
            found_any=true
            log_result "⚠️  POSSÍVEL DUPLICAÇÃO: $pattern"
            for script in "${scripts[@]}"; do
                if find "$SCRIPTS_DIR" -name "$script" -type f | grep -q .; then
                    local full_path=$(find "$SCRIPTS_DIR" -name "$script" -type f)
                    log_result "   📄 $full_path"
                fi
            done
            log_result ""
        fi
    done

    if [ "$found_any" = true ]; then
        log_result "🔴 IMPACTO: Múltiplos scripts com propósitos similares causam confusão e manutenção duplicada"
        log_result "💡 SOLUÇÃO: Consolidar em um único script com múltiplas opções\n"
    else
        log_result "✅ Nenhum script com nomes similares encontrado\n"
    fi
}

# ============================================================================
# AUDITORIA 4: Funções de Validação/Verificação Duplicadas
# ============================================================================

audit_validation_functions() {
    print_header "[4/6] AUDITORIA: Funções de Validação/Verificação Duplicadas"

    log_result "🔍 Procurando funções de validação (check_, validate_, verify_)...\n"

    local validation_functions=()

    while IFS= read -r line; do
        validation_functions+=("$line")
    done < <(grep -rh "^[a-z_]*\(check\|validate\|verify\)[a-z_]*\s*()" "$SCRIPTS_DIR" --include="*.sh" 2>/dev/null | sort | uniq -c | sort -rn)

    if [ ${#validation_functions[@]} -gt 0 ]; then
        log_result "📊 Funções de validação encontradas:\n"
        for func in "${validation_functions[@]}"; do
            log_result "   $func"
        done
        log_result "\n💡 RECOMENDAÇÃO: Consolidar funções similares em biblioteca comum\n"
    else
        log_result "✅ Nenhuma duplicação significativa de funções de validação\n"
    fi
}

# ============================================================================
# AUDITORIA 5: Cleanup Scripts Redundantes
# ============================================================================

audit_cleanup_scripts() {
    print_header "[5/6] AUDITORIA: Scripts de Cleanup Redundantes"

    log_result "🔍 Procurando scripts de cleanup...\n"

    local cleanup_scripts=(
        "cleanup_all_backups.sh"
        "cleanup_obsolete.sh"
        "cleanup_project.sh"
        "cleanup_temp_files.sh"
    )

    local found_count=0

    for script in "${cleanup_scripts[@]}"; do
        if find "$SCRIPTS_DIR" -name "$script" -type f | grep -q .; then
            ((found_count++))
            log_result "   📄 $script"
        fi
    done

    if [ $found_count -gt 1 ]; then
        log_result "\n⚠️  DUPLICAÇÃO ENCONTRADA: $found_count scripts de cleanup"
        log_result "🔴 IMPACTO: Múltiplos scripts de cleanup causam confusão sobre qual usar"
        log_result "💡 SOLUÇÃO: Criar 'cleanup.sh' unificado com opções (--all, --obsolete, --temp, --backups)\n"
    else
        log_result "\n✅ Cleanup scripts bem organizados\n"
    fi
}

# ============================================================================
# AUDITORIA 6: Análise de Tamanho e Complexidade
# ============================================================================

audit_size_complexity() {
    print_header "[6/6] AUDITORIA: Tamanho e Complexidade dos Scripts"

    log_result "🔍 Analisando tamanho e linhas de código...\n"

    local large_scripts=()

    while IFS= read -r file; do
        local lines=$(wc -l < "$file")
        if [ "$lines" -gt 300 ]; then
            large_scripts+=("$file:$lines")
        fi
    done < <(find "$SCRIPTS_DIR" -name "*.sh" -type f)

    if [ ${#large_scripts[@]} -gt 0 ]; then
        log_result "⚠️  SCRIPTS GRANDES (>300 linhas) - Possível consolidação:\n"
        for item in "${large_scripts[@]}"; do
            IFS=':' read -r file lines <<< "$item"
            log_result "   📄 $(basename "$file") - $lines linhas"
        done
        log_result "\n🔴 IMPACTO: Scripts muito grandes são difíceis de manter e testar"
        log_result "💡 SOLUÇÃO: Dividir em módulos menores com funções bem definidas\n"
    else
        log_result "✅ Nenhum script excessivamente grande\n"
    fi
}

# ============================================================================
# RESUMO FINAL
# ============================================================================

print_summary() {
    print_header "RESUMO EXECUTIVO - AUDITORIA DE DUPLICAÇÕES"

    log_result "📋 Relatório completo salvo em: $REPORT_FILE\n"

    log_result "🎯 RECOMENDAÇÕES PRIORITÁRIAS:\n"
    log_result "   1. Criar biblioteca comum de funções (scripts/lib/)"
    log_result "   2. Consolidar scripts de logging e cores"
    log_result "   3. Unificar cleanup scripts"
    log_result "   4. Revisar scripts com nomes similares"
    log_result "   5. Dividir scripts muito grandes\n"

    log_result "✨ Benefícios esperados após refatoração:"
    log_result "   • Redução de ~30-40% no tamanho total dos scripts"
    log_result "   • Manutenção centralizada de funções comuns"
    log_result "   • Melhor desempenho (menos parsing de código duplicado)"
    log_result "   • Código mais legível e testável\n"
}

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

main() {
    echo -e "${BOLD}${CYAN}"
    cat << "EOF"
╔════════════════════════════════════════════════════════════════╗
║          AUDITORIA DE SCRIPTS - DETECÇÃO DE DUPLICAÇÕES       ║
║              Análise de Desempenho e Manutenção               ║
╚════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"

    # Inicializar relatório
    > "$REPORT_FILE"

    # Executar auditorias
    audit_logging_functions
    audit_color_definitions
    audit_similar_names
    audit_validation_functions
    audit_cleanup_scripts
    audit_size_complexity

    # Resumo
    print_summary
}

main "$@"
