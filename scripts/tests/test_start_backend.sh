#!/bin/bash
# =============================================================================
# Script de Teste para start_backend.sh
# =============================================================================
# Executa testes de validação do script de inicialização do SILA System
# =============================================================================

set -euo pipefail

# Definição de Cores para Output
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# Localização: O script assume que está em scripts/tests/
# O root do projeto está dois níveis acima
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_SCRIPT="$PROJECT_ROOT/scripts/start_backend.sh"

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
echo "   Teste do Script start_backend.sh"
echo "=============================================="
echo "Raiz do Projeto: $PROJECT_ROOT"
echo ""

# Teste 1: Arquivo existe
echo "Teste 1: Verificando se script existe..."
if [ -f "$TARGET_SCRIPT" ]; then
    test_result "Script start_backend.sh existe" 0
else
    test_result "Script start_backend.sh existe" 1
fi

# Teste 2: Script tem permissão de execução
echo "Teste 2: Verificando permissões..."
if [ -x "$TARGET_SCRIPT" ]; then
    test_result "Script é executável" 0
else
    echo -e "${YELLOW}⚠️  Script não é executável. Ajustando...${NC}"
    chmod +x "$TARGET_SCRIPT" 2>/dev/null || true
    [ -x "$TARGET_SCRIPT" ] && test_result "Script ajustado para executável" 0 || test_result "Permissão de execução" 1
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

# Teste 5: Arquivos docker-compose existem no root
echo "Teste 5: Verificando arquivos docker-compose..."
if [ -f "$PROJECT_ROOT/docker-compose.yml" ]; then
    test_result "docker-compose.yml existe" 0
else
    test_result "docker-compose.yml existe" 1
fi

# Teste 6: Sintaxe bash do script
echo "Teste 6: Verificando sintaxe bash..."
if bash -n "$TARGET_SCRIPT" 2>/dev/null; then
    test_result "Sintaxe bash válida" 0
else
    test_result "Sintaxe bash válida" 1
fi

# Teste 8: Diretórios necessários para o Backend
echo "Teste 8: Verificando estrutura de diretórios do backend..."
REQUIRED_DIRS=("$PROJECT_ROOT/apps/backend" "$PROJECT_ROOT/apps/backend/app")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        test_result "Diretório $(basename "$dir") existe" 0
    else
        test_result "Diretório $(basename "$dir") existe" 1
    fi
done

# Teste 9: Arquivo .env existe no backend
echo "Teste 9: Verificando arquivos .env no backend..."
if [ -f "$PROJECT_ROOT/apps/backend/.env" ] || [ -f "$PROJECT_ROOT/apps/backend/.env.example" ]; then
    test_result "Ambiente (.env ou .env.example) encontrado" 0
else
    test_result "Ambiente encontrado" 1
fi

# Teste 10: Backend Dockerfile existe
echo "Teste 10: Verificando Dockerfile do backend..."
if [ -f "$PROJECT_ROOT/apps/backend/Dockerfile" ]; then
    test_result "Backend Dockerfile existe" 0
else
    test_result "Backend Dockerfile existe" 1
fi

# Resumo Final
echo ""
echo "=============================================="
echo "   Resumo dos Testes"
echo "=============================================="
echo -e "${GREEN}✅ Testes passados: $TEST_PASSED${NC}"
echo -e "${RED}❌ Testes falhados: $TEST_FAILED${NC}"
echo ""

if [ $TEST_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 Tudo pronto para iniciar o Backend!${NC}"
    echo ""
    echo "Comandos recomendados:"
    echo "  1. Ir para a raiz: cd $PROJECT_ROOT"
    echo "  2. Executar: bash scripts/start_backend.sh"
    exit 0
else
    echo -e "${RED}⚠️  Alguns testes falharam. Corrija-os para evitar regressões.${NC}"
    exit 1
fi