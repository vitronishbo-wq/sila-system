#!/usr/bin/env bash
set -euo pipefail

echo "🔍 SILA Dependency Audit"
echo "=============================="

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

PYTHON=python3
REQ_FILE="$ROOT_DIR/requirements.txt"
VALIDATOR="$ROOT_DIR/automation/validation/dependency_validator.py"

echo "▶ Verificando ambiente Python..."
$PYTHON --version

echo "▶ Validando requirements.txt..."
$PYTHON "$VALIDATOR" || {
    echo "❌ Validação de dependências falhou"
    exit 1
}

echo "▶ Verificando conflitos (pip check)..."
pip check || {
    echo "❌ Conflitos detectados"
    exit 1
}

echo "▶ Auditoria de segurança (pip-audit)..."
pip-audit || {
    echo "⚠️ Vulnerabilidades encontradas (revise a lista acima)"
}

echo "✔ Auditoria concluída com sucesso."
