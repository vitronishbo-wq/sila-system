#!/bin/bash
# backend/entrypoint.sh
# ==============================================
# Script de inicialização do backend SILA
# - Espera o DB ficar pronto
# - Aplica migrações Alembic se disponível
# - Define PYTHONPATH corretamente
# - Inicia o servidor FastAPI
# ==============================================

set -euo pipefail

# ============================
# FUNÇÃO: Esperar DB
# ============================
wait_for_db() {
    echo "📦 Aguardando DB ficar pronto (até 60s)..."

    if [ -n "${DATABASE_URL:-}" ]; then
        echo "🔎 DATABASE_URL detectada, usando para esperar DB..."
        python - <<'PY'
import os, time, urllib.parse as up, socket, sys
url = os.environ.get("DATABASE_URL")
parsed = up.urlparse(url)
host = parsed.hostname or "db"
port = parsed.port or 5432
print(f"⏱️  Esperando {host}:{port} ...")
start = time.time()
while time.time() - start < 60:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("✅ DB pronto")
            sys.exit(0)
    except Exception:
        time.sleep(1)
print("⚠️ Timeout esperando DB")
sys.exit(2)
PY
        return $?
    else
        host="db"
        port=5432
        n=0
        while [ $n -lt 60 ]; do
            if nc -z "$host" "$port" >/dev/null 2>&1; then
                echo "✅ DB pronto"
                return 0
            fi
            n=$((n+1))
            sleep 1
        done
        echo "⚠️ Timeout esperando DB"
        return 2
    fi
}

wait_for_db || echo "⚠️ Prosseguindo mesmo com DB possivelmente indisponível"

# ============================
# CONFIGURAR PYTHONPATH E DIRETÓRIO
# ============================
if [ -d "/app" ]; then
    export PYTHONPATH="/app:$(dirname /app):${PYTHONPATH:-}"
    cd /app
elif [ -d "/code" ]; then
    export PYTHONPATH="/code:$(dirname /code):${PYTHONPATH:-}"
    cd /code
fi

# ============================
# APLICAR MIGRAÇÕES ALEMBIC
# ============================
if command -v alembic >/dev/null 2>&1 && [ -f "alembic.ini" ]; then
    echo "📦 Aplicando migrações Alembic..."
    if ! alembic upgrade head; then
        echo "⚠️ Falha em alembic upgrade; tentando stamp head..."
        alembic stamp head || true
        alembic upgrade head || echo "⚠️ Alembic ainda falhou; prosseguindo"
    fi
else
    if ! command -v alembic >/dev/null 2>&1; then
        echo "ℹ️ Alembic não encontrado; pulando migrações"
    elif [ ! -f "alembic.ini" ]; then
        echo "ℹ️ alembic.ini não encontrado em $(pwd); pulando migrações"
    fi
fi

# ============================
# INICIAR SERVIDOR
# ============================
PORT="${PORT:-8000}"
ENVIRONMENT="${ENVIRONMENT:-development}"
export PORT

echo "🚀 Iniciando FastAPI na porta $PORT em modo $ENVIRONMENT..."

# Verificar se está em modo desenvolvimento para ativar hot reload
if [ "$ENVIRONMENT" = "development" ] || [ "$DEBUG" = "true" ]; then
    echo "🔥 Modo desenvolvimento - Hot reload ativado"
    exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --reload --reload-dir /app
else
    echo "🏭 Modo produção - Servidor otimizado"
    exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --workers 4
fi
