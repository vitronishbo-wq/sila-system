#!/usr/bin/env bash
set -euo pipefail

MODULES_ROOT="apps/backend/app/modules"
REPORT_DIR="reports"
TIMESTAMP="$(date -u +%Y%m%d_%H%M%S)"
COLLECT_LOG="${REPORT_DIR}/test_collect_${TIMESTAMP}.log"
GHOST_LOG="${REPORT_DIR}/test_import_ghosts_${TIMESTAMP}.log"
PATTERN="comercio_externo|financas_impostos|pescas_industriais|portos_logistica|transportes_logistica"

mkdir -p "${REPORT_DIR}"

echo "=== TEST COHERENCE SCAN ==="
echo "[1/2] pytest --collect-only ${MODULES_ROOT}"
set +e
pytest --collect-only "${MODULES_ROOT}" >"${COLLECT_LOG}" 2>&1
collect_status=$?
set -e
echo "collect_exit_code=${collect_status}"
echo "collect_log=${COLLECT_LOG}"

echo "[2/2] grep imports fantasmas em */tests"
mapfile -t test_dirs < <(find "${MODULES_ROOT}" -type d -name tests | sort)
if [ ${#test_dirs[@]} -eq 0 ]; then
    echo "Nenhum diretorio de testes encontrado sob ${MODULES_ROOT}" | tee "${GHOST_LOG}"
    ghost_status=0
else
    set +e
    grep -rE --line-number "${PATTERN}" "${test_dirs[@]}" >"${GHOST_LOG}"
    ghost_status=$?
    set -e
fi
echo "ghost_scan_exit_code=${ghost_status}"
echo "ghost_log=${GHOST_LOG}"

if [ "${ghost_status}" -eq 1 ]; then
    echo "ghost_matches=0"
else
    if [ -s "${GHOST_LOG}" ]; then
        echo "ghost_matches>0"
        sed -n '1,120p' "${GHOST_LOG}"
    else
        echo "ghost_matches=0"
    fi
fi

echo "=== TEST COHERENCE SCAN DONE ==="
