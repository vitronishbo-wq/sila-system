#!/usr/bin/env bash
set -euo pipefail

# Use inherited ROOT_DIR if available, otherwise calculate it
if [[ -z "${ROOT_DIR:-}" ]]; then
  ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
fi
cd "$ROOT_DIR"

echo "== Guardrails de Consolidação =="
echo "Working directory: $(pwd)"

fail=0

echo "[1/6] Verificando placeholders no admin frontend..."
if rg -n "em construção" apps/frontend/src/App.tsx >/dev/null; then
  echo "ERRO: ainda existem rotas admin em construção no App.tsx"
  rg -n "em construção" apps/frontend/src/App.tsx
  fail=1
else
  echo "OK: sem placeholders de rotas admin no App.tsx"
fi

echo "[2/6] Verificando identidades mock do workflow..."
if rg -n "00000000-0000-0000-0000-00000000000" apps/backend/app/modules/workflow/api/router.py >/dev/null; then
  echo "ERRO: workflow ainda contém UUIDs mock hardcoded"
  rg -n "00000000-0000-0000-0000-00000000000" apps/backend/app/modules/workflow/api/router.py
  fail=1
else
  echo "OK: sem UUID mock no workflow router"
fi

echo "[3/6] Verificando imports legados diretos de app.citizen..."
legacy_count="$( (rg -n "from app\\.citizen|import app\\.citizen" apps/backend/app || true) | wc -l | tr -d ' ' )"
echo "INFO: imports legados encontrados: ${legacy_count}"

echo "[4/6] Verificando se saude_primaria está montado no main..."
if rg -n "app\\.include_router\\(saude_router\\)" apps/backend/app/main.py >/dev/null; then
  echo "OK: saude_primaria montado no main.py"
else
  echo "ERRO: saude_primaria não está montado no main.py"
  fail=1
fi

echo "[5/6] Verificando uso de run_sync (strict async)..."
runtime_run_sync_matches="$(
  rg -n "run_sync\\(" apps/backend/app \
    -g "!**/tests/**" \
    -g "!**/test_*.py" \
    -g "!**/conftest.py" \
    -g "!**/validate_integration.py" || true
)"
runtime_run_sync_hits="$(printf "%s\n" "$runtime_run_sync_matches" | sed '/^$/d' | wc -l | tr -d ' ')"
if [[ "$runtime_run_sync_hits" -gt 0 ]]; then
  echo "WARN: run_sync em código runtime (${runtime_run_sync_hits} ocorrências)."
  printf "%s\n" "$runtime_run_sync_matches"
  if [[ "${STRICT_ASYNC:-0}" == "1" ]]; then
    echo "ERRO: STRICT_ASYNC=1 ativo e run_sync runtime detectado."
    fail=1
  fi
else
  echo "OK: sem run_sync em código runtime."
fi

test_tooling_run_sync_matches="$(
  rg -n "run_sync\\(" apps/backend/app \
    -g "**/tests/**" \
    -g "**/test_*.py" \
    -g "**/conftest.py" \
    -g "**/validate_integration.py" || true
)"
test_tooling_run_sync_hits="$(printf "%s\n" "$test_tooling_run_sync_matches" | sed '/^$/d' | wc -l | tr -d ' ')"
if [[ "$test_tooling_run_sync_hits" -gt 0 ]]; then
  echo "INFO: run_sync em testes/tooling (${test_tooling_run_sync_hits} ocorrências)."
  printf "%s\n" "$test_tooling_run_sync_matches"
fi

echo "[6/6] Verificando uso de Session síncrona no workflow..."
if rg -n "from sqlalchemy\\.orm import Session" apps/backend/app/modules/workflow >/dev/null; then
  echo "WARN: Session síncrona ainda encontrada no módulo workflow."
  rg -n "from sqlalchemy\\.orm import Session" apps/backend/app/modules/workflow || true
  if [[ "${STRICT_ASYNC:-0}" == "1" ]]; then
    echo "ERRO: STRICT_ASYNC=1 ativo e Session síncrona detectada."
    fail=1
  fi
else
  echo "OK: workflow sem import de Session síncrona."
fi

if [[ "$fail" -ne 0 ]]; then
  echo "Falha nos guardrails."
  exit 1
fi

echo "Guardrails passaram."
