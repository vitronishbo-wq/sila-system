#!/usr/bin/env bash
# 🚀 Inicializador Rápido do Sistema SILA
# Script para facilitar o uso do sistema completo

echo "🎯 Sistema SILA - Inicialização Rápida"
echo "======================================"

# Verificar se estamos no diretório correto
if [[ ! "$(pwd)" =~ sila-system ]]; then
    if [ -d "/opt/sila-system" ]; then
        echo "📁 Movendo para diretório do SILA..."
        cd /opt/sila-system
    else
        echo "❌ Diretório /opt/sila-system não encontrado"
        echo "💡 Execute: cd /opt/sila-system && ./automation/utils/listar_codigo.sh"
        exit 1
    fi
fi

echo "📍 Diretório atual: $(pwd)"

# Verificar se o script mestre existe
if [ ! -f "automation/utils/listar_codigo.sh" ]; then
    echo "❌ Script mestre não encontrado em automation/utils/"
    exit 1
fi

# Executar sistema completo
echo "🚀 Executando Sistema SILA completo..."
./automation/utils/listar_codigo.sh
