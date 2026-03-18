#!/bin/bash

################################################################################
# SILA NGINX - Script de Validação
# Testa se o nginx_automation.sh está funcionando corretamente
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

# Contadores
tests_total=0
tests_passed=0
tests_failed=0

# Função de teste
run_test() {
    local test_name="$1"
    local command="$2"

    tests_total=$((tests_total + 1))

    echo -e "\n${BLUE}Test $tests_total: $test_name${NC}"
    echo "Command: $command"

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASSOU${NC}"
        tests_passed=$((tests_passed + 1))
    else
        echo -e "${RED}❌ FALHOU${NC}"
        tests_failed=$((tests_failed + 1))
    fi
}

# Header
echo -e "${BOLD}${BLUE}"
cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                   SILA NGINX - Teste de Validação                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Testes
echo -e "\n${BOLD}📋 TESTES DE ESTRUTURA${NC}"

run_test "Script nginx_automation.sh existe" \
    "test -f '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script é executável" \
    "test -x '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Diretório apps/backend existe" \
    "test -d '$SCRIPT_DIR/apps/backend'"

run_test "Diretório apps/frontend existe" \
    "test -d '$SCRIPT_DIR/apps/frontend'"

run_test "Diretório infrastructure/docker existe" \
    "test -d '$SCRIPT_DIR/infrastructure/docker'"

echo -e "\n${BOLD}📄 TESTES DE DOCUMENTAÇÃO${NC}"

run_test "NGINX_AUTOMATION_GUIDE.md existe" \
    "test -f '$SCRIPT_DIR/NGINX_AUTOMATION_GUIDE.md'"

run_test "NGINX_CHEATSHEET.md existe" \
    "test -f '$SCRIPT_DIR/NGINX_CHEATSHEET.md'"

run_test "NGINX_REFINEMENT_SUMMARY.md existe" \
    "test -f '$SCRIPT_DIR/NGINX_REFINEMENT_SUMMARY.md'"

echo -e "\n${BOLD}🔍 TESTES DE CONTEÚDO${NC}"

run_test "Script contém função detect_services" \
    "grep -q 'detect_services()' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém função generate_nginx_config" \
    "grep -q 'generate_nginx_config()' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém função validate_nginx_config" \
    "grep -q 'validate_nginx_config()' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém função diagnose_nginx_issue" \
    "grep -q 'diagnose_nginx_issue()' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém função help_text" \
    "grep -q 'help_text()' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém comando --auto" \
    "grep -q '\--auto' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém comando --generate" \
    "grep -q '\--generate' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém comando --diagnose" \
    "grep -q '\--diagnose' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém comando --validate-config" \
    "grep -q '\--validate-config' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém variável APPS_DIR" \
    "grep -q 'APPS_DIR=' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém variável BACKEND_DIR" \
    "grep -q 'BACKEND_DIR=' '$SCRIPT_DIR/nginx_automation.sh'"

run_test "Script contém variável FRONTEND_DIR" \
    "grep -q 'FRONTEND_DIR=' '$SCRIPT_DIR/nginx_automation.sh'"

echo -e "\n${BOLD}🧪 TESTES DE EXECUÇÃO (Sem deploy)${NC}"

run_test "Script mostra ajuda" \
    "bash '$SCRIPT_DIR/nginx_automation.sh' --help | grep -q 'PARA LEIGOS'"

run_test "Script detecta serviços" \
    "bash '$SCRIPT_DIR/nginx_automation.sh' --list-services | grep -q 'Backend\\|Frontend'"

# Resultado final
echo -e "\n${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}📊 RESUMO DOS TESTES${NC}"
echo -e "Total: $tests_total"
echo -e "${GREEN}Passou: $tests_passed${NC}"
echo -e "${RED}Falhou: $tests_failed${NC}"

if [[ $tests_failed -eq 0 ]]; then
    echo -e "\n${GREEN}${BOLD}✅ TODOS OS TESTES PASSARAM!${NC}"
    exit 0
else
    echo -e "\n${RED}${BOLD}❌ ALGUNS TESTES FALHARAM${NC}"
    exit 1
fi
