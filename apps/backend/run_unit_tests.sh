#!/bin/bash
"""
Script para executar testes unitários e verificar cobertura

Este script executa todos os testes unitários criados e gera
relatório de cobertura para acompanhar o progresso da Fase 3.1.
"""

set -e

echo "🧪 Executando Testes Unitários - Fase 3.1"
echo "=========================================="

# Mudar para diretório do backend
cd /opt/sila-system/backend

echo ""
echo "📊 Verificando estrutura de testes..."
echo "=================================="

# Verificar se pytest está disponível
if ! python -m pytest --version > /dev/null 2>&1; then
    echo "❌ pytest não encontrado. Instalando dependências..."
    pip install pytest pytest-asyncio pytest-cov coverage
fi

# Verificar se backend está no Python path
echo "🔍 Verificando imports..."
python -c "import backend.core.config; print('✅ Backend imports OK')" 2>/dev/null || {
    echo "❌ Problema com imports do backend"
    export PYTHONPATH="$PYTHONPATH:$(pwd)"
    echo "✅ PYTHONPATH atualizado"
}

echo ""
echo "🚀 Executando testes unitários..."
echo "================================"

# Executar testes unitários com cobertura
python -m pytest tests/unit/ \
    -v \
    --tb=short \
    --cov=backend \
    --cov-report=term-missing \
    --cov-report=html:htmlcov_unit \
    --cov-report=xml:coverage_unit.xml \
    --cov-fail-under=0 \
    -m "unit" \
    2>&1 | tee test_results.log

echo ""
echo "📈 Resultados da Cobertura:"
echo "=========================="

# Verificar se foi gerado relatório de cobertura
if [ -f "htmlcov_unit/index.html" ]; then
    echo "✅ Relatório HTML gerado: htmlcov_unit/index.html"
fi

if [ -f "coverage_unit.xml" ]; then
    echo "✅ Relatório XML gerado: coverage_unit.xml"
fi

# Extrair métricas de cobertura
if [ -f "test_results.log" ]; then
    echo ""
    echo "📋 Resumo dos Testes:"
    echo "===================="

    # Contar testes executados
    TOTAL_TESTS=$(grep -c "PASSED\|FAILED\|ERROR" test_results.log | grep -v "===")
    PASSED_TESTS=$(grep -c "PASSED" test_results.log)
    FAILED_TESTS=$(grep -c "FAILED\|ERROR" test_results.log)

    echo "Total de testes: $TOTAL_TESTS"
    echo "✅ Passaram: $PASSED_TESTS"
    echo "❌ Falharam: $FAILED_TESTS"

    if [ "$FAILED_TESTS" -eq 0 ]; then
        echo "🎉 Todos os testes passaram!"
    else
        echo "⚠️  Alguns testes falharam. Verifique test_results.log"
    fi
fi

# Verificar cobertura específica dos módulos testados
echo ""
echo "🔍 Cobertura por Módulo:"
echo "======================="

if command -v coverage > /dev/null 2>&1; then
    # Gerar relatório de cobertura específico
    coverage report --include="backend/modules/auth/*,backend/core/*,backend/modules/notifications/*" --omit="*/tests/*,*/test_*" || echo "⚠️  Não foi possível gerar relatório de cobertura específico"
else
    echo "⚠️  Coverage CLI não disponível"
fi

echo ""
echo "📁 Arquivos de Teste Criados:"
echo "============================"
find tests/unit/ -name "test_*.py" | sort

echo ""
echo "✅ Fase 3.1 - Testes Unitários Executados!"
echo "=========================================="

if [ -f "test_results.log" ]; then
    echo ""
    echo "📄 Log detalhado salvo em: test_results.log"
fi

echo ""
echo "🎯 Próximos Passos:"
echo "- Implementar mais testes para alcançar 70% de cobertura"
echo "- Adicionar testes para lógica de negócio crítica"
echo "- Configurar CI/CD para executar testes automaticamente"
