#!/bin/bash

echo "======================================"
echo "📚 SILA SYSTEM - VERIFICANDO DOCUMENTAÇÃO"
echo "======================================"

# Verificar se backend está rodando
echo "🔍 Verificando se o backend está rodando..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend está respondendo"
else
    echo "❌ Backend não está respondendo"
    echo "🚀 Iniciando backend..."
    cd /opt/sila-system/backend
    python main.py &
    sleep 3
fi

# Verificar documentação
echo "📚 Verificando documentação Swagger..."
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ Documentação está ativa!"
    echo "🌐 Acesse: http://localhost:8000/docs"
    echo "📗 Alternative: http://localhost:8000/redoc"
else
    echo "❌ Documentação não encontrada"
    echo "🔄 Verificando configuração..."

    # Verificar configuração no main.py
    if grep -q "docs_url=\"/docs\"" main.py; then
        echo "✅ Configuração parece correta"
        echo "🔄 Reiniciando servidor..."
        pkill -f "python main.py" 2>/dev/null || true
        sleep 2
        python main.py &
        sleep 3

        # Testar novamente
        if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
            echo "✅ Documentação ativada com sucesso!"
            echo "🌐 Acesse: http://localhost:8000/docs"
        else
            echo "❌ Problema persiste. Verificando logs..."
            tail -20 app.log 2>/dev/null || echo "Nenhum log encontrado"
        fi
    else
        echo "❌ Configuração do main.py precisa ser corrigida"
    fi
fi

echo "======================================"
