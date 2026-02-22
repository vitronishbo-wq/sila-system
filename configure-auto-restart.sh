#!/bin/bash
# ========================================
# SILA System - Configuração de Auto-Restart
# Garante que containers reiniciem automaticamente
# ========================================

set -e

echo "🇦🇴 SILA System - Configuração de Auto-Restart"
echo "=========================================="

# Containers para configurar
CONTAINERS=(
    "sila-db"
    "sila-redis"
    "sila-backend"
    "sila-frontend"
    "sila-celery"
)

echo "🔄 Configurando política de restart para containers..."
echo ""

for container in "${CONTAINERS[@]}"; do
    if docker ps -a --format '{{.Names}}' | grep -q "^${container}$"; then
        docker update --restart always "$container"
        echo "✅ ${container}: restart policy = always"
    else
        echo "⚠️  ${container}: container não encontrado"
    fi
done

echo ""
echo "=========================================="
echo "✅ Configuração concluída!"
echo ""
echo "📋 Política de Restart:"
echo "   - Os containers reiniciarão automaticamente após:"
echo "     • Falhas/crashes"
echo "     • Reinicialização do servidor"
echo "     • Reinicialização do Docker daemon"
echo ""
echo "🔍 Verificar status:"
echo "   docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.RestartPolicy}}'"
echo ""
echo "🇦🇴 Sistema protegido contra quedas de energia!"
echo "=========================================="
