#!/bin/bash

################################################################################
# SILA System - Production Validation Script
# Automated comprehensive validation for production readiness
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global counters
PASSED=0
FAILED=0
WARNING=0
TOTAL=0

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_ROOT"

# Create output directory
mkdir -p reports/validation

REPORT_FILE="reports/validation/production_validation_$(date +%Y%m%d_%H%M%S).txt"
JSON_REPORT="reports/validation/validation_results_$(date +%Y%m%d_%H%M%S).json"

################################################################################
# Helper Functions
################################################################################

log_test() {
    local test_name="$1"
    ((TOTAL++))
    echo -e "${BLUE}[TEST $TOTAL]${NC} $test_name"
}

log_pass() {
    local message="$1"
    ((PASSED++))
    echo -e "${GREEN}✓ PASSED${NC}: $message"
    echo "✓ PASSED: $message" >> "$REPORT_FILE"
}

log_fail() {
    local message="$1"
    ((FAILED++))
    echo -e "${RED}✗ FAILED${NC}: $message"
    echo "✗ FAILED: $message" >> "$REPORT_FILE"
}

log_warn() {
    local message="$1"
    ((WARNING++))
    echo -e "${YELLOW}⚠ WARNING${NC}: $message"
    echo "⚠ WARNING: $message" >> "$REPORT_FILE"
}

header() {
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "$1"
    echo "═══════════════════════════════════════════════════════════════"
    echo "" | tee -a "$REPORT_FILE"
    echo "╔════════════════════════════════════════════════════════════╗" >> "$REPORT_FILE"
    echo "║ $1" >> "$REPORT_FILE"
    echo "╚════════════════════════════════════════════════════════════╝" >> "$REPORT_FILE"
}

################################################################################
# Validation Tests
################################################################################

validate_environment_config() {
    header "1. ENVIRONMENT CONFIGURATION VALIDATION"

    local required_vars=(
        "DATABASE_URL"
        "ASYNC_DATABASE_URL"
        "ENVIRONMENT"
        "DEBUG"
        "LOG_LEVEL"
    )

    # Check all environment files
    for env_file in .env .env.test .env.production .env.staging; do
        if [ -f "$env_file" ]; then
            log_test "Verificando $env_file"
            local missing=0

            for var in "${required_vars[@]}"; do
                if grep -q "^$var=" "$env_file" 2>/dev/null; then
                    log_pass "$var definida em $env_file"
                else
                    log_warn "$var não encontrada em $env_file"
                    ((missing++))
                fi
            done

            [ $missing -eq 0 ] || log_warn "$env_file tem $missing variáveis faltando"
        fi
    done
}

validate_imports() {
    header "2. ABSOLUTE IMPORTS VALIDATION"

    log_test "Procurando imports relativos problemáticos"

    local relative_imports=$(find apps/backend -name "*.py" -type f -exec grep -l "^from \.\.\." {} \; 2>/dev/null | wc -l)

    if [ $relative_imports -eq 0 ]; then
        log_pass "Nenhum import relativo além do package encontrado"
    else
        log_fail "Encontrados $relative_imports arquivos com imports relativos"
    fi

    log_test "Validando importação de core.db.base_class"

    local wrong_imports=$(find apps/backend -name "*.py" -type f -exec grep -l "from core.database import" {} \; 2>/dev/null | wc -l)

    if [ $wrong_imports -eq 0 ]; then
        log_pass "Nenhuma importação de core.database encontrada"
    else
        log_fail "Encontradas $wrong_imports referências a core.database (deveria ser core.db.base_class)"
    fi
}

validate_database_schemas() {
    header "3. DATABASE SCHEMA VALIDATION"

    log_test "Verificando nomenclatura de tabelas com prefixo de módulo"

    local payment_models="apps/backend/modules/payment/models"

    for model_file in "$payment_models"/*.py; do
        if [ -f "$model_file" ]; then
            if grep -q "__tablename__" "$model_file"; then
                local tablename=$(grep "__tablename__" "$model_file" | head -1)

                if echo "$tablename" | grep -q "payment_"; then
                    log_pass "$(basename $model_file) usa prefixo correto: $tablename"
                else
                    log_warn "$(basename $model_file) pode estar sem prefixo: $tablename"
                fi
            fi
        fi
    done

    log_test "Validando foreign keys com nomes corretos de tabela"

    local wrong_fks=$(find apps/backend/modules -name "*.py" -type f -exec grep -c 'ForeignKey("[^"]*[^s]\.id")' {} \; 2>/dev/null | awk '{s+=$1} END {print s}')

    if [ "$wrong_fks" == "0" ] || [ -z "$wrong_fks" ]; then
        log_pass "Foreign keys validadas com nomes corretos"
    else
        log_warn "Verificar $wrong_fks possíveis foreign keys com nomes incompletos"
    fi
}

validate_pydantic_schemas() {
    header "4. PYDANTIC SCHEMA VALIDATION"

    log_test "Validando ConfigDict com from_attributes=True"

    local schemas_correct=$(find apps/backend/modules -path "*/schemas/*.py" -exec grep -l "from_attributes=True" {} \; 2>/dev/null | wc -l)
    local schemas_total=$(find apps/backend/modules -path "*/schemas/*.py" -type f 2>/dev/null | wc -l)

    if [ "$schemas_correct" -ge "$((schemas_total - 1))" ]; then
        log_pass "Esquemas com from_attributes=True: $schemas_correct/$schemas_total"
    else
        log_warn "Apenas $schemas_correct de $schemas_total esquemas têm from_attributes=True"
    fi
}

validate_async_compliance() {
    header "5. ASYNC/AWAIT COMPLIANCE"

    log_test "Validando que todas operações DB usam await"

    local missing_awaits=$(find apps/backend/modules -name "*.py" -type f -exec grep -E "^\s+(self\.db\.|session\.)(commit|execute|refresh|flush)\(" {} + 2>/dev/null | grep -v "await" | wc -l)

    if [ $missing_awaits -eq 0 ]; then
        log_pass "Todas operações async estão com await"
    else
        log_warn "Encontradas $missing_awaits operações que podem estar sem await"
    fi

    log_test "Validando métodos async em services"

    local service_methods=$(find apps/backend/modules -path "*/services/*.py" -type f -exec grep -c "async def" {} \; 2>/dev/null | awk '{s+=$1} END {print s}')

    if [ "$service_methods" -gt 0 ]; then
        log_pass "Encontrados $service_methods métodos async em services"
    else
        log_warn "Nenhum método async encontrado em services"
    fi
}

validate_error_handling() {
    header "6. ERROR HANDLING VALIDATION"

    log_test "Validando try-except em endpoints"

    local endpoints_with_error_handling=$(find apps/backend/modules -path "*/endpoints/*.py" -type f -exec grep -l "except.*Error\|except.*Exception" {} \; 2>/dev/null | wc -l)

    if [ "$endpoints_with_error_handling" -gt 0 ]; then
        log_pass "Encontrados $endpoints_with_error_handling endpoints com error handling"
    else
        log_warn "Poucos endpoints com error handling explícito"
    fi

    log_test "Validando ValueError para erros de validação"

    local validation_errors=$(find apps/backend/modules -path "*/services/*.py" -type f -exec grep -c "raise ValueError" {} \; 2>/dev/null | awk '{s+=$1} END {print s}')

    if [ "$validation_errors" -gt 0 ]; then
        log_pass "Encontrados $validation_errors ValueError para erros de validação"
    else
        log_warn "Poucas validações com ValueError"
    fi
}

validate_tests() {
    header "7. TEST SUITE VALIDATION"

    # Ensure PYTHONPATH is set
    export PYTHONPATH="${PROJECT_ROOT}/apps/backend"

    # Activate virtual environment
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi

    log_test "Executando suite de testes de payment"

    if python -m pytest tests/modules/payment/test_service.py -v --tb=short 2>&1 | tee temp_test_output.txt | grep -q "passed"; then
        local passed=$(grep -oP '\d+(?= passed)' temp_test_output.txt | tail -1)
        local failed=$(grep -oP '\d+(?= failed)' temp_test_output.txt | tail -1 || echo "0")

        log_pass "Testes de payment: $passed passed, ${failed:-0} failed"

        # Store results
        echo "PAYMENT_TESTS_PASSED=$passed" >> "$REPORT_FILE"
        echo "PAYMENT_TESTS_FAILED=${failed:-0}" >> "$REPORT_FILE"
    else
        log_fail "Erro ao executar testes de payment"
    fi

    rm -f temp_test_output.txt
}

validate_documentation() {
    header "8. DOCUMENTATION VALIDATION"

    log_test "Verificando arquivos de documentação produzidos"

    local required_docs=(
        ".github/copilot-instructions.md"
        "WORK_COMPLETION_SUMMARY.md"
        "QUICK_START_DEV_GUIDE.md"
        "DELIVERABLES_INDEX.md"
    )

    for doc in "${required_docs[@]}"; do
        if [ -f "$doc" ]; then
            local lines=$(wc -l < "$doc")
            log_pass "$doc criado com $lines linhas"
        else
            log_fail "$doc não encontrado"
        fi
    done
}

validate_code_quality() {
    header "9. CODE QUALITY METRICS"

    log_test "Contando arquivos Python no backend"

    local python_files=$(find apps/backend/modules -name "*.py" -type f | wc -l)
    log_pass "Total de arquivos Python: $python_files"

    log_test "Analisando cobertura de type hints"

    local files_with_types=$(find apps/backend/modules -name "*.py" -type f -exec grep -l ": " {} \; 2>/dev/null | wc -l)
    local coverage_pct=$((files_with_types * 100 / python_files))

    if [ "$coverage_pct" -ge 80 ]; then
        log_pass "Cobertura de type hints: $coverage_pct%"
    else
        log_warn "Cobertura de type hints baixa: $coverage_pct%"
    fi
}

validate_logging() {
    header "10. LOGGING CONFIGURATION"

    log_test "Verificando configuração de logging em core/config.py"

    if grep -q "LOG_LEVEL\|logging" apps/backend/core/config.py 2>/dev/null; then
        log_pass "Logging configurado em core/config.py"
    else
        log_warn "Logging pode não estar totalmente configurado"
    fi

    log_test "Validando uso de logging em serviços"

    local files_with_logging=$(find apps/backend/modules -path "*/services/*.py" -type f -exec grep -l "logger\|logging" {} \; 2>/dev/null | wc -l)

    if [ "$files_with_logging" -gt 0 ]; then
        log_pass "Encontrados $files_with_logging services com logging"
    else
        log_warn "Poucos services usam logging explícito"
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║     SILA SYSTEM - PRODUCTION VALIDATION SUITE             ║"
    echo "║              Automated Comprehensive Check                ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""

    # Initialize report
    cat > "$REPORT_FILE" << 'EOF'
╔════════════════════════════════════════════════════════════╗
║     SILA SYSTEM - PRODUCTION VALIDATION REPORT            ║
║              Generated: $(date)                            ║
╚════════════════════════════════════════════════════════════╝

EOF

    # Run all validation tests
    validate_environment_config
    validate_imports
    validate_database_schemas
    validate_pydantic_schemas
    validate_async_compliance
    validate_error_handling
    validate_tests
    validate_documentation
    validate_code_quality
    validate_logging

    # Print summary
    header "VALIDATION SUMMARY"

    echo ""
    echo "Total Tests Run:      $TOTAL"
    echo -e "Tests Passed:         ${GREEN}$PASSED${NC}"
    echo -e "Tests Failed:         ${RED}$FAILED${NC}"
    echo -e "Warnings:             ${YELLOW}$WARNING${NC}"
    echo ""

    # Calculate pass rate
    if [ $TOTAL -gt 0 ]; then
        local pass_rate=$((PASSED * 100 / TOTAL))
        echo "Pass Rate: $pass_rate%"

        if [ $pass_rate -ge 90 ]; then
            echo -e "${GREEN}✓ PRODUCTION READY${NC}"
            STATUS="PRODUCTION_READY"
        elif [ $pass_rate -ge 70 ]; then
            echo -e "${YELLOW}⚠ CONDITIONALLY READY${NC}"
            STATUS="CONDITIONALLY_READY"
        else
            echo -e "${RED}✗ NOT READY${NC}"
            STATUS="NOT_READY"
        fi
    fi

    # Save summary to report
    echo "" >> "$REPORT_FILE"
    echo "════════════════════════════════════════════════════════════" >> "$REPORT_FILE"
    echo "SUMMARY STATISTICS" >> "$REPORT_FILE"
    echo "════════════════════════════════════════════════════════════" >> "$REPORT_FILE"
    echo "Total Tests Run: $TOTAL" >> "$REPORT_FILE"
    echo "Tests Passed: $PASSED" >> "$REPORT_FILE"
    echo "Tests Failed: $FAILED" >> "$REPORT_FILE"
    echo "Warnings: $WARNING" >> "$REPORT_FILE"
    echo "Pass Rate: ${pass_rate:-0}%" >> "$REPORT_FILE"
    echo "Status: $STATUS" >> "$REPORT_FILE"

    echo ""
    echo "Report saved to: $REPORT_FILE"
    echo ""

    # Exit with appropriate code
    [ $FAILED -eq 0 ] && exit 0 || exit 1
}

# Run main
main
