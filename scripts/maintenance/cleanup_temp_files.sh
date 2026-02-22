#!/bin/bash
set -euo pipefail

# Importar bibliotecas de cores/logging se existirem
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
[ -f "$SCRIPT_DIR/../lib/colors.sh" ] && source "$SCRIPT_DIR/../lib/colors.sh"
[ -f "$SCRIPT_DIR/../lib/logging.sh" ] && source "$SCRIPT_DIR/../lib/logging.sh"

log_info() { echo -e "\e[34m[INFO]\e[0m $1"; }
log_success() { echo -e "\e[32m[SUCCESS]\e[0m $1"; }

log_info "🧹 Iniciando limpeza profunda de arquivos temporários..."

# 1. Limpeza Python
log_info "Removendo artefatos Python (__pycache__, .pyc, .pyo)..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.py[co]" -delete 2>/dev/null || true

# 2. Limpeza Frontend
log_info "Removendo pastas de build e cache de frontend..."
rm -rf apps/frontend/dist
rm -rf apps/frontend/.vite
rm -rf apps/frontend/node_modules/.cache

# 3. Limpeza de Logs e Temporários do Sistema
log_info "Limpando arquivos de log e backups temporários..."
rm -f apps/backend/*.log
rm -f scripts/migration/*.log
rm -rf .pytest_cache
rm -rf .ruff_cache
rm -rf .mypy_cache

# 4. Limpeza Docker (Opcional - apenas containers parados)
log_info "Limpando containers órfãos e caches de build..."
docker system prune -f --filter "label=project=sila" 2>/dev/null || true

log_success "✨ Limpeza concluída com sucesso!"