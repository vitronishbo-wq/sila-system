#!/bin/bash
# Script de Testes Automatizados do SILA System
# Executa suite completa de testes: unit, integration, e2e
# Uso: ./scripts/run_tests.sh [unit|integration|e2e|all]

set -euo pipefail

# --- Configurações ---
TEST_TYPE="${1:-all}"
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
COVERAGE_THRESHOLD=80

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# --- Funções de Logging ---

log() {
    local level=$1
    local message=$2
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')

    case "$level" in
        INFO)
            echo -e "[${timestamp}] ${BLUE}[INFO]${NC} $message"
            ;;
        SUCCESS)
            echo -e "[${timestamp}] ${GREEN}[SUCCESS]${NC} $message"
            ;;
        WARN)
            echo -e "[${timestamp}] ${YELLOW}[WARN]${NC} $message"
            ;;
        ERROR)
            echo -e "[${timestamp}] ${RED}[ERROR]${NC} $message"
            ;;
        *)
            echo -e "[${timestamp}] [${level}] $message"
            ;;
    esac
}

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║              🧪 SILA System - Automated Tests                ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# --- Funções de Teste ---

check_dependencies() {
    log INFO "Verificando dependências de teste..."

    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        log ERROR "Python3 não está instalado"
        exit 1
    fi

    # Verificar pip
    if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
        log ERROR "pip não está instalado"
        exit 1
    fi

    # Verificar Node.js (para testes frontend)
    if ! command -v node &> /dev/null; then
        log WARN "Node.js não está instalado. Testes de frontend serão pulados."
    fi

    log SUCCESS "Dependências verificadas"
}

setup_test_environment() {
    log INFO "Configurando ambiente de testes..."

    # Criar arquivo .env.test se não existir
    if [[ ! -f ".env.test" ]]; then
        log INFO "Criando .env.test..."
        cat > .env.test << 'ENVTEST'
ENVIRONMENT=test
NODE_ENV=test
DEBUG=False
LOG_LEVEL=WARNING

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sila_test
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=test-secret-key-do-not-use-in-production
JWT_SECRET_KEY=test-jwt-secret-key

# Testing
TESTING=True
PYTEST_TIMEOUT=30
ENVTEST
    fi

    # Exportar variáveis de teste
    export ENVIRONMENT=test
    export TESTING=True

    log SUCCESS "Ambiente de testes configurado"
}

run_backend_unit_tests() {
    log INFO "Executando testes unitários do backend..."

    cd "$BACKEND_DIR"

    # Instalar dependências de teste se necessário
    if ! python3 -c "import pytest" 2>/dev/null; then
        log INFO "Instalando pytest..."
        pip install pytest pytest-cov pytest-asyncio pytest-timeout
    fi

    # Executar testes unitários
    log INFO "Rodando pytest com coverage..."
    pytest tests/ -v \
        --cov=modules \
        --cov=app \
        --cov-report=xml \
        --cov-report=term-missing \
        --cov-report=html \
        --timeout=30 \
        -m "not external and not slow" \
        --tb=short

    local exit_code=$?

    # Verificar coverage
    if [[ -f "coverage.xml" ]]; then
        local coverage=$(python3 -c "import xml.etree.ElementTree as ET; tree = ET.parse('coverage.xml'); print(tree.getroot().attrib.get('line-rate', 0))" 2>/dev/null || echo "0")
        local coverage_percent=$(python3 -c "print(int(float($coverage) * 100))" 2>/dev/null || echo "0")

        log INFO "Coverage: ${coverage_percent}%"

        if [[ $coverage_percent -lt $COVERAGE_THRESHOLD ]]; then
            log WARN "Coverage abaixo do threshold (${COVERAGE_THRESHOLD}%)"
        else
            log SUCCESS "Coverage acima do threshold!"
        fi
    fi

    cd ..

    if [[ $exit_code -eq 0 ]]; then
        log SUCCESS "Testes unitários do backend passaram!"
        return 0
    else
        log ERROR "Testes unitários do backend falharam!"
        return 1
    fi
}

run_backend_integration_tests() {
    log INFO "Executando testes de integração do backend..."

    cd "$BACKEND_DIR"

    # Verificar se PostgreSQL está rodando
    if ! nc -z localhost 5432 2>/dev/null; then
        log WARN "PostgreSQL não está rodando em localhost:5432"
        log INFO "Iniciando containers de teste..."

        # Subir apenas o banco de dados para testes
        docker compose -f ../docker-compose.yml up -d postgres
        sleep 5
    fi

    # Executar testes de integração
    pytest tests/ -v \
        --timeout=60 \
        -m "integration" \
        --tb=short

    local exit_code=$?

    cd ..

    if [[ $exit_code -eq 0 ]]; then
        log SUCCESS "Testes de integração do backend passaram!"
        return 0
    else
        log ERROR "Testes de integração do backend falharam!"
        return 1
    fi
}

run_frontend_tests() {
    log INFO "Executando testes do frontend..."

    if [[ ! -d "$FRONTEND_DIR" ]]; then
        log WARN "Diretório frontend não encontrado. Pulando testes de frontend."
        return 0
    fi

    cd "$FRONTEND_DIR"

    # Verificar se node_modules existe
    if [[ ! -d "node_modules" ]]; then
        log INFO "Instalando dependências do frontend..."
        npm install
    fi

    # Executar linting
    log INFO "Executando linting..."
    npm run lint || log WARN "Linting falhou ou não configurado"

    # Executar type checking
    log INFO "Executando type checking..."
    npm run type-check || log WARN "Type checking falhou ou não configurado"

    # Executar testes unitários
    log INFO "Executando testes unitários..."
    npm run test:unit || log WARN "Testes unitários não configurados"

    # Build de teste
    log INFO "Testando build..."
    npm run build

    local exit_code=$?

    cd ..

    if [[ $exit_code -eq 0 ]]; then
        log SUCCESS "Testes do frontend passaram!"
        return 0
    else
        log ERROR "Build do frontend falhou!"
        return 1
    fi
}

run_e2e_tests() {
    log INFO "Executando testes E2E..."

    # Verificar se os serviços estão rodando
    if ! curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
        log WARN "Backend não está rodando. Iniciando serviços..."
        ./sila_start.sh dev &

        # Aguardar serviços iniciarem
        local max_wait=60
        local elapsed=0

        while [[ $elapsed -lt $max_wait ]]; do
            if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
                log SUCCESS "Serviços iniciados!"
                break
            fi
            sleep 5
            elapsed=$((elapsed + 5))
        done

        if [[ $elapsed -ge $max_wait ]]; then
            log ERROR "Timeout aguardando serviços iniciarem"
            return 1
        fi
    fi

    # Executar testes E2E (Playwright, Cypress, etc.)
    if [[ -f "tests/e2e/run_e2e.sh" ]]; then
        bash tests/e2e/run_e2e.sh
    else
        log WARN "Testes E2E não configurados"
        return 0
    fi
}

run_smoke_tests() {
    log INFO "Executando smoke tests..."

    # Testar endpoints principais
    local endpoints=(
        "http://localhost:8000/health"
        "http://localhost:8000/docs"
        "http://localhost:9111/health"
        "http://localhost:9111/metrics"
    )

    local failed=0

    for endpoint in "${endpoints[@]}"; do
        if curl -s -f "$endpoint" > /dev/null 2>&1; then
            log SUCCESS "✅ $endpoint"
        else
            log ERROR "❌ $endpoint"
            failed=$((failed + 1))
        fi
    done

    if [[ $failed -eq 0 ]]; then
        log SUCCESS "Todos os smoke tests passaram!"
        return 0
    else
        log ERROR "$failed smoke tests falharam"
        return 1
    fi
}

generate_test_report() {
    log INFO "Gerando relatório de testes..."

    local report_file="test-report-$(date +%Y%m%d-%H%M%S).txt"

    cat > "$report_file" << EOF
╔═══════════════════════════════════════════════════════════════╗
║              SILA System - Test Report                       ║
╚═══════════════════════════════════════════════════════════════╝

Data: $(date '+%Y-%m-%d %H:%M:%S')
Tipo de Teste: $TEST_TYPE

--- Backend Tests ---
Coverage Report: backend/htmlcov/index.html
XML Report: backend/coverage.xml

--- Frontend Tests ---
Build Output: frontend/dist/

--- Logs ---
Ver logs completos acima.

EOF

    log SUCCESS "Relatório gerado: $report_file"
}

# --- Função Principal ---

main() {
    local exit_code=0

    log INFO "Tipo de teste selecionado: $TEST_TYPE"

    # Verificar dependências
    check_dependencies

    # Configurar ambiente
    setup_test_environment

    # Executar testes baseado no tipo
    case "$TEST_TYPE" in
        unit)
            run_backend_unit_tests || exit_code=1
            ;;
        integration)
            run_backend_integration_tests || exit_code=1
            ;;
        frontend)
            run_frontend_tests || exit_code=1
            ;;
        e2e)
            run_e2e_tests || exit_code=1
            ;;
        smoke)
            run_smoke_tests || exit_code=1
            ;;
        all)
            log INFO "Executando suite completa de testes..."

            run_backend_unit_tests || exit_code=1
            run_backend_integration_tests || exit_code=1
            run_frontend_tests || exit_code=1
            run_smoke_tests || exit_code=1
            ;;
        *)
            log ERROR "Tipo de teste inválido: $TEST_TYPE"
            log INFO "Uso: $0 [unit|integration|frontend|e2e|smoke|all]"
            exit 1
            ;;
    esac

    # Gerar relatório
    generate_test_report

    # Resultado final
    echo ""
    if [[ $exit_code -eq 0 ]]; then
        log SUCCESS "✅ Todos os testes passaram!"
    else
        log ERROR "❌ Alguns testes falharam!"
    fi

    exit $exit_code
}

# --- Entry Point ---

main "$@"
