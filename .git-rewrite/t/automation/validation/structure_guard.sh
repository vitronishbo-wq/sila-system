#!/usr/bin/env bash
set -euo pipefail

# 🛡️ SILA Structure Guard
# Executa guardrails estruturais do monorepo: paths, imports e .env.
# Pode ser integrado em CI ou em targets do Makefile.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "${ROOT_DIR}"

echo "🛡️  SILA Structure Guard"
echo "============================"

run_check() {
  local label="$1"; shift
  echo "\n▶ ${label}"
  if "$@"; then
    echo "✅ ${label} OK"
  else
    echo "❌ ${label} falhou"
    return 1
  fi
}

run_check "Path consistency" python3 tools/consistency/check_paths.py
run_check "Import topology" python3 tools/consistency/check_imports.py
run_check "Env files" python3 tools/consistency/check_env_files.py

echo "\n🎯 Structure guard concluído com sucesso."
