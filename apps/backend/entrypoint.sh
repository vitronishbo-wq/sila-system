#!/bin/bash
set -eo pipefail

# 1. Função de espera determinística (Apenas leitura de rede)
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    echo "⏳ [DIAGNÓSTICO] Aguardando $service ($host:$port)..."
    while ! nc -z "$host" "$port"; do
      sleep 1
    done
    echo "✅ $service detetado e operacional."
}

# Aguardar dependências críticas
wait_for_service "db" "5432" "PostgreSQL"

if [[ "$CELERY_BROKER_URL" == *"redis"* ]]; then
    wait_for_service "redis" "6379" "Redis"
fi

# 2. Configuração de Ambiente Estrita
export PYTHONPATH=/app
# Força o Python a não escrever ficheiros .pyc (artefactos inúteis) dentro do container
export PYTHONDONTWRITEBYTECODE=1

# 3. Migrações (Apenas se solicitado)
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "🔄 [ESTADO] Sincronizando esquema da base de dados..."
    alembic upgrade head
else
    echo "⚠️ [AVISO] Migrações saltadas por configuração."
fi

# 4. Execução limpa
# Removidos: mkdir e chmod (Devem ser tratados via Dockerfile/Volumes)
echo "🚀 [SILA] Executando comando: $@"
exec "$@"