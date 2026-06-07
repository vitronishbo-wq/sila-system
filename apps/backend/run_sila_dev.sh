#!/bin/bash
# SILA System - Development Server Launcher
# Roda com força total no WSL2 (metal puro, sem Docker overhead)

set -e

cd "$(dirname "$0")"

echo "🚀 Iniciando SILA System API..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📍 Ambiente: WSL2 - Acesso direto ao processador"
echo "🔥 Mode: Development com Hot Reload"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Ativa venv
source /home/dev03wsl/sila-system/.venv/bin/activate

# Variáveis de ambiente
export PYTHONUNBUFFERED=1
export API_ENV=development
export LOG_LEVEL=INFO

# Inicia servidor com uvicorn
# --reload: Hot reload automático
# --workers 1: Suficiente para dev
# --log-level info: Logs estruturados
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info

echo ""
echo "✅ Servidor parado"
