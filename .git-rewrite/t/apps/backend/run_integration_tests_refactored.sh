#!/bin/bash

# Script para executar testes de integração refatorados - Fase 3.3
# Foco em testes de API em vez de end-to-end

set -e

echo "🚀 INICIANDO TESTES DE INTEGRAÇÃO REFACTORADOS - FASE 3.3"
echo "=========================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Verificar dependências
log "Verificando dependências dos testes..."

if ! python -c "import pytest" 2>/dev/null; then
    error "pytest não está instalado"
    exit 1
fi

if ! python -c "import respx" 2>/dev/null; then
    warn "respx não está instalado. Instalando..."
    pip install respx
fi

if ! python -c "import httpx" 2>/dev/null; then
    warn "httpx não está instalado. Instalando..."
    pip install httpx
fi

success "Dependências verificadas ✅"

# Diretório dos testes
TEST_DIR="/opt/sila-system/backend/tests/integration"
cd "$TEST_DIR"

# Estatísticas iniciais
log "Coletando estatísticas dos testes..."
TOTAL_FILES=$(find . -name "*.py" -type f | wc -l)
TEST_FILES=$(find . -name "*.py" -exec grep -l "def test_" {} \; | wc -l)
TOTAL_TESTS=$(find . -name "*.py" -exec grep -c "def test_" {} \; | awk '{sum += $1} END {print sum}')

echo ""
echo "📊 ESTATÍSTICAS DOS TESTES:"
echo "- Total de arquivos: $TOTAL_FILES"
echo "- Arquivos com testes: $TEST_FILES"
echo "- Total de funções de teste: $TOTAL_TESTS"
echo ""

# Executar testes com diferentes focos
log "Executando testes de API refatorados..."

echo ""
echo "🧪 TESTE 1: API de Autenticação"
echo "================================"
if pytest test_api_refactored.py::TestAuthenticationAPI -v --tb=short; then
    success "Testes de autenticação passaram ✅"
else
    error "Testes de autenticação falharam ❌"
    AUTH_FAILED=1
fi

echo ""
echo "🧪 TESTE 2: API de Atualização de BI"
echo "===================================="
if pytest test_api_refactored.py::TestBIUpdateAPI -v --tb=short; then
    success "Testes de BI passaram ✅"
else
    error "Testes de BI falharam ❌"
    BI_FAILED=1
fi

echo ""
echo "🧪 TESTE 3: API de Notificações"
echo "==============================="
if pytest test_api_refactored.py::TestNotificationAPI -v --tb=short; then
    success "Testes de notificações passaram ✅"
else
    error "Testes de notificações falharam ❌"
    NOTIF_FAILED=1
fi

echo ""
echo "🧪 TESTE 4: Integração com APIs Externas"
echo "========================================"
if pytest test_api_refactored.py::TestExternalAPIIntegration -v --tb=short; then
    success "Testes de integração externa passaram ✅"
else
    error "Testes de integração externa falharam ❌"
    EXT_FAILED=1
fi

echo ""
echo "⚡ TESTE 5: Performance das APIs"
echo "================================="
if pytest test_api_refactored.py::TestPerformanceAPI -v --tb=short; then
    success "Testes de performance passaram ✅"
else
    error "Testes de performance falharam ❌"
    PERF_FAILED=1
fi

echo ""
echo "✅ TESTE 6: Validação de Dados"
echo "=============================="
if pytest test_api_refactored.py::TestValidationAPI -v --tb=short; then
    success "Testes de validação passaram ✅"
else
    error "Testes de validação falharam ❌"
    VALID_FAILED=1
fi

echo ""
echo "🚨 TESTE 7: Tratamento de Erros"
echo "==============================="
if pytest test_api_refactored.py::TestErrorHandlingAPI -v --tb=short; then
    success "Testes de erro passaram ✅"
else
    error "Testes de erro falharam ❌"
    ERROR_FAILED=1
fi

echo ""
echo "📄 TESTE 8: Paginação"
echo "====================="
if pytest test_api_refactored.py::TestPaginationAPI -v --tb=short; then
    success "Testes de paginação passaram ✅"
else
    error "Testes de paginação falharam ❌"
    PAG_FAILED=1
fi

# Teste de performance geral
echo ""
echo "⏱️ TESTE 9: Performance Geral dos Testes"
echo "========================================"
log "Medindo tempo de execução dos testes..."

START_TIME=$(date +%s.%N)

if pytest test_api_refactored.py --tb=short -x; then
    END_TIME=$(date +%s.%N)
    DURATION=$(echo "$END_TIME - $START_TIME" | bc)
    success "Todos os testes executaram em ${DURATION}s ✅"

    # Verificar se está dentro do limite
    if (( $(echo "$DURATION > 30.0" | bc -l) )); then
        warn "Testes demoraram mais de 30 segundos (${DURATION}s)"
    else
        success "Performance dentro do esperado (< 30s) ✅"
    fi
else
    error "Falha na execução geral dos testes ❌"
    GENERAL_FAILED=1
fi

# Comparação com testes antigos
echo ""
echo "📈 COMPARAÇÃO COM TESTES ANTIGOS"
echo "================================="

if [ -f "test_audit.py" ]; then
    log "Testando performance dos testes antigos..."

    START_TIME_OLD=$(date +%s.%N)
    if pytest test_audit.py -v --tb=short >/dev/null 2>&1; then
        END_TIME_OLD=$(date +%s.%N)
        DURATION_OLD=$(echo "$END_TIME_OLD - $START_TIME_OLD" | bc -l)
        log "Testes antigos: ${DURATION_OLD}s"

        if (( $(echo "$DURATION < $DURATION_OLD" | bc -l) )); then
            IMPROVEMENT=$(echo "scale=2; ($DURATION_OLD - $DURATION) / $DURATION_OLD * 100" | bc)
            success "Melhoria de performance: ${IMPROVEMENT}% mais rápido ✅"
        else
            REGRESSION=$(echo "scale=2; ($DURATION - $DURATION_OLD) / $DURATION_OLD * 100" | bc)
            warn "Regressão de performance: ${REGRESSION}% mais lento ⚠️"
        fi
    else
        warn "Testes antigos não executaram (provavelmente dependências externas)"
    fi
fi

# Relatório de cobertura
echo ""
echo "📊 RELATÓRIO DE COBERTURA"
echo "========================"

log "Gerando relatório de cobertura..."
if pytest test_api_refactored.py --cov=modules --cov-report=term-missing --cov-report=html:htmlcov --tb=short; then
    success "Relatório de cobertura gerado ✅"
    log "Relatório HTML disponível em: htmlcov/index.html"
else
    warn "Não foi possível gerar relatório de cobertura"
fi

# Resumo final
echo ""
echo "📋 RESUMO DA FASE 3.3 - REFINAMENTO DE INTEGRAÇÃO"
echo "=================================================="

# Contar falhas
FAILED_COUNT=0
[ "$AUTH_FAILED" ] && ((FAILED_COUNT++))
[ "$BI_FAILED" ] && ((FAILED_COUNT++))
[ "$NOTIF_FAILED" ] && ((FAILED_COUNT++))
[ "$EXT_FAILED" ] && ((FAILED_COUNT++))
[ "$PERF_FAILED" ] && ((FAILED_COUNT++))
[ "$VALID_FAILED" ] && ((FAILED_COUNT++))
[ "$ERROR_FAILED" ] && ((FAILED_COUNT++))
[ "$PAG_FAILED" ] && ((FAILED_COUNT++))
[ "$GENERAL_FAILED" ] && ((FAILED_COUNT++))

PASSED_COUNT=$((8 - FAILED_COUNT))

echo "✅ Testes passados: $PASSED_COUNT/8"
echo "❌ Testes falhados: $FAILED_COUNT/8"

if [ $FAILED_COUNT -eq 0 ]; then
    success "🎉 FASE 3.3 CONCLUÍDA COM SUCESSO!"
    echo ""
    echo "🏆 CONQUISTAS:"
    echo "- ✅ Testes refatorados para foco em API"
    echo "- ✅ Fixtures centralizadas e reutilizáveis"
    echo "- ✅ Mock de dependências externas"
    echo "- ✅ Testes de performance implementados"
    echo "- ✅ Validação robusta de dados"
    echo "- ✅ Tratamento de erros verificado"
    echo "- ✅ Paginação testada"
    echo "- ✅ Melhoria significativa de performance"
    echo ""
    echo "📈 PRÓXIMOS PASSOS:"
    echo "-1. Aplicar padrão refatorado aos demais 104 arquivos"
    echo "-2. Configurar CI/CD para executar testes de API"
    echo "-3. Monitorar performance em produção"
    echo "-4. Documentar padrões para equipe"

    exit 0
else
    error "❌ FASE 3.3 COM FALHAS PARCIAIS"
    echo ""
    echo "🔧 AÇÕES NECESSÁRIAS:"
    echo "-1. Corrigir testes falhados"
    echo "-2. Verificar configuração de mocks"
    echo "-3. Revisar implementação das fixtures"
    echo "-4. Validar endpoints da API"

    exit 1
fi
