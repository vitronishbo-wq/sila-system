#!/bin/bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
BACKEND_DIR="apps/backend"
MODULES_DIR="${BACKEND_DIR}/modules"
TESTS_DIR="tests"
REQUIREMENTS_FILE="${BACKEND_DIR}/requirements.txt"
ALEMBIC_DIR="${BACKEND_DIR}/alembic"
PYTHON_EXEC="python3"

# Check if running in CI environment
if [ -n "${CI:-}" ]; then
    echo -e "${YELLOW}⚠️  Running in CI environment - some checks may be skipped${NC}"
    CI_MODE=true
else
    CI_MODE=false
fi

echo -e "🔍 ${GREEN}Iniciando diagnóstico completo do backend${NC}"
echo "=================================================="

# 1. Environment and Python setup
echo -e "\n[1/8] ${GREEN}Ambiente Python e Dependências${NC}"
echo "----------------------------------------"
${PYTHON_EXEC} --version
${PYTHON_EXEC} -m pip --version

# 2. Check virtual environment
echo -e "\n[2/8] ${GREEN}Verificando ambiente virtual${NC}"
echo "----------------------------------------"
if [ -n "${VIRTUAL_ENV:-}" ]; then
    echo -e "✅ Ambiente virtual ativo: ${VIRTUAL_ENV}"
else
    echo -e "⚠️  ${YELLOW}Nenhum ambiente virtual ativo detectado${NC}"
    if [ "$CI_MODE" = false ]; then
        read -p "Deseja criar e ativar um ambiente virtual? (s/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            ${PYTHON_EXEC} -m venv .venv
            source .venv/bin/activate
            echo "✅ Ambiente virtual ativado"
        fi
    fi
fi

# 3. Install/update dependencies
echo -e "\n[3/8] ${GREEN}Verificando dependências${NC}"
echo "----------------------------------------"
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Instalando/atualizando dependências de $REQUIREMENTS_FILE"
    ${PYTHON_EXEC} -m pip install -r "$REQUIREMENTS_FILE"
    echo -e "✅ Dependências instaladas/atualizadas"
else
    echo -e "⚠️  ${YELLOW}Arquivo de requisitos não encontrado em $REQUIREMENTS_FILE${NC}"
fi

# 4. Check database migrations
echo -e "\n[4/8] ${GREEN}Verificando migrações do banco de dados${NC}"
echo "----------------------------------------"
if [ -d "$ALEMBIC_DIR" ]; then
    if command -v alembic &> /dev/null; then
        echo "Últimas migrações:"
        (cd "$BACKEND_DIR" && alembic history | tail -n 5 || echo -e "${YELLOW}⚠️  Erro ao verificar histórico do Alembic${NC}")

        if [ "$CI_MODE" = false ]; then
            read -p "Deseja verificar se há migrações pendentes? (s/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Ss]$ ]]; then
                (cd "$BACKEND_DIR" && alembic current || echo -e "${YELLOW}⚠️  Erro ao verificar migrações pendentes${NC}")
            fi
        fi
    else
        echo -e "⚠️  ${YELLOW}Alembic não está instalado${NC}"
    fi
else
    echo -e "⚠️  ${YELLOW}Diretório de migrações não encontrado em $ALEMBIC_DIR${NC}"
fi

# 5. Check for duplicate tables and models
echo -e "\n[5/8] ${GREEN}Verificando duplicações de tabelas e modelos${NC}"
echo "----------------------------------------"
if [ -d "$MODULES_DIR" ]; then
    echo "Procurando por modelos duplicados..."

    # Find all model files and check for duplicate class names
    find "$MODULES_DIR" -name "*.py" -type f -exec grep -l "class " {} \; | while read -r file; do
        grep -h "^class " "$file" | awk '{print $2}' | tr -d '(:' | while read -r class_name; do
            echo "$class_name $file"
        done
done | sort | uniq -w 50 | awk '{
    count[$1]++;
    if (count[$1] == 1) first[$1] = $0;
    if (count[$1] == 2) print "\n" first[$1];
    if (count[$1] >= 1) print $0;
}' | grep -v "^$" && echo -e "✅ Nenhuma duplicação encontrada" || true
else
    echo -e "⚠️  ${YELLOW}Diretório de módulos não encontrado em $MODULES_DIR${NC}"
fi

# 6. Run tests for all modules
echo -e "\n[6/8] ${GREEN}Executando testes${NC}"
echo "----------------------------------------"
if [ -d "$TESTS_DIR" ]; then
    echo "Encontrados os seguintes módulos de teste:"
    find "$TESTS_DIR/modules" -maxdepth 1 -mindepth 1 -type d -exec basename {} \; | sort

    # Run tests with coverage if available
    if command -v pytest &> /dev/null; then
        echo -e "\nExecutando testes..."
        PYTHONPATH="${PYTHONPATH:-}:"${PWD}"" \
        pytest -v --cov="$MODULES_DIR" --cov-report=term-missing "$TESTS_DIR"
    else
        echo -e "⚠️  ${YELLOW}pytest não está instalado. Instale com 'pip install pytest pytest-cov'${NC}"
    fi
else
    echo -e "⚠️  ${YELLOW}Diretório de testes não encontrado em $TESTS_DIR${NC}"
fi

# 7. Check for broken imports
echo -e "\n[7/8] ${GREEN}Verificando imports quebrados${NC}"
echo "----------------------------------------"
if [ -d "$MODULES_DIR" ]; then
    echo "Verificando erros de sintaxe..."
    find "$MODULES_DIR" -name "*.py" -type f -print0 | xargs -0 ${PYTHON_EXEC} -m py_compile

    if [ $? -eq 0 ]; then
        echo -e "✅ Nenhum erro de sintaxe encontrado"
    else
        echo -e "⚠️  ${YELLOW}Erros de sintaxe encontrados nos módulos${NC}"
    fi

    # Clean up .pyc files
    find "$MODULES_DIR" -name "*.pyc" -delete
else
    echo -e "⚠️  ${YELLOW}Diretório de módulos não encontrado em $MODULES_DIR${NC}"
fi

# 8. Check for common security issues
echo -e "\n[8/8] ${GREEN}Verificações de segurança básicas${NC}"
echo "----------------------------------------"
# Check for hardcoded secrets
SECRET_PATTERNS=("password" "secret" "api[_-]?key" "token" "credential")

echo "Verificando possíveis segredos em código..."
for pattern in "${SECRET_PATTERNS[@]}"; do
    grep -rI --color=always --include="*.py" --include="*.env" --include="*.yaml" --include="*.yml" -n "$pattern" "$BACKEND_DIR" | grep -v "#" | grep -v "password=" || true
done

echo -e "\n✅ ${GREEN}Diagnóstico completo!${NC}"
echo "=================================================="

# Final check for critical issues
if [ "$CI_MODE" = true ] && [ -n "${GITHUB_ACTIONS:-}" ]; then
    # In CI, fail if there are test failures
    if [ -f ".coverage" ]; then
        coverage report --fail-under=80
    fi

    # Add any additional CI-specific checks here
    echo "::set-output name=status::success"
fi

exit 0
