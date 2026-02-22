#!/bin/bash
# =============================================================================
# Script de Teste para start_backend.sh
# =============================================================================
# Executa testes de validação do script de inicialização
# =============================================================================

set -euo pipefail

readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_PASSED=0
TEST_FAILED=0

test_result() {
    local name="$1"
    local result="$2"

    if [ "$result" = "0" ]; then
        echo -e "${GREEN}✅ PASS${NC}: $name"
        TEST_PASSED=$((TEST_PASSED + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: $name"
        TEST_FAILED=$((TEST_FAILED + 1))
    fi
}

echo "=============================================="
echo "  Teste do Script start_backend.sh"
echo "=============================================="
echo ""

# Teste 1: Arquivo existe
echo "Teste 1: Verificando se script existe..."
if [ -f "$SCRIPT_DIR/start_backend.sh" ]; then
    test_result "Script existe" 0
else
    test_result "Script existe" 1
fi

# Teste 2: Script tem permissão de execução
echo "Teste 2: Verificando permissões..."
if [ -x "$SCRIPT_DIR/start_backend.sh" ]; then
    test_result "Script é executável" 0
else
    echo -e "${YELLOW}⚠️  Script não é executável. Ajustando...${NC}"
    chmod +x "$SCRIPT_DIR/start_backend.sh"
    test_result "Script ajustado para executável" 0
fi

# Teste 3: Docker está instalado
echo "Teste 3: Verificando Docker..."
if command -v docker &> /dev/null; then
    test_result "Docker instalado" 0
else
    test_result "Docker instalado" 1
fi

# Teste 4: Docker Compose está disponível
echo "Teste 4: Verificando Docker Compose..."
if docker compose version &> /dev/null; then
    test_result "Docker Compose disponível" 0
else
    test_result "Docker Compose disponível" 1
fi

# Teste 5: Arquivos docker-compose existem
echo "Teste 5: Verificando arquivos docker-compose..."
COMPOSE_FILES=("docker-compose.yml")
for file in "${COMPOSE_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        test_result "$file existe" 0
    else
        test_result "$file existe" 1
    fi
done

# Teste 6: Sintaxe bash do script
echo "Teste 6: Verificando sintaxe bash..."
if bash -n "$SCRIPT_DIR/start_backend.sh" 2>/dev/null; then
    test_result "Sintaxe bash válida" 0
else
    test_result "Sintaxe bash válida" 1
fi

# Teste 7: Dry run do script
echo "Teste 7: Executando dry run..."
if DRY_RUN=true bash "$SCRIPT_DIR/start_backend.sh" &> /dev/null; then
    test_result "Dry run executado" 0
else
    test_result "Dry run executado" 1
fi

# Teste 8: Diretórios necessários
echo "Teste 8: Verificando estrutura de diretórios..."
REQUIRED_DIRS=("backend" "backend/app")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$SCRIPT_DIR/$dir" ]; then
        test_result "Diretório $dir existe" 0
    else
        test_result "Diretório $dir existe" 1
    fi
done

# Teste 9: Arquivo .env existe
echo "Teste 9: Verificando arquivos .env..."
if [ -f "$SCRIPT_DIR/.env" ] || [ -f "$SCRIPT_DIR/.env.development" ]; then
    test_result "Arquivo .env encontrado" 0
else
    test_result "Arquivo .env encontrado" 1
fi

# Teste 10: Backend Dockerfile existe
echo "Teste 10: Verificando Dockerfile do backend..."
if [ -f "$SCRIPT_DIR/backend/Dockerfile" ]; then
    test_result "Backend Dockerfile existe" 0
else
    test_result "Backend Dockerfile existe" 1
fi

# Resumo
echo ""
echo "=============================================="
echo "  Resumo dos Testes"
echo "=============================================="
echo -e "${GREEN}✅ Testes passados: $TEST_PASSED${NC}"
echo -e "${RED}❌ Testes falhados: $TEST_FAILED${NC}"
echo ""

if [ $TEST_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 Todos os testes passaram!${NC}"
    echo ""
    echo "Você pode executar o script com:"
    echo "  bash start_backend.sh"
    echo ""
    echo "Ou com opções:"
    echo "  APP_ENV=production bash start_backend.sh"
    echo "  BACKUP_MODE=always bash start_backend.sh"
    echo "  FORCE_REBUILD=true bash start_backend.sh"
    exit 0
else
    echo -e "${RED}⚠️  Alguns testes falharam. Verifique os erros acima.${NC}"
    exit 1
fi
