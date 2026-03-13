#!/bin/bash
set -e

echo "Analisando integridade das fronteiras..."
lint-imports --config .import-linter
lint_status=$?

echo "Verificando arquivos espurios..."
stale_targets=()
if [ -d "app/modules" ]; then
    stale_targets+=("app/modules")
fi
if [ -d "apps/backend/app/modules" ]; then
    stale_targets+=("apps/backend/app/modules")
fi

if [ ${#stale_targets[@]} -gt 0 ]; then
    stale_files=$(find "${stale_targets[@]}" -type f \( -name "*.bak" -o -name "*.old" -o -name "*_backup_*" -o -name "*_temp_*" \))
    if [ -n "$stale_files" ]; then
        echo "Arquivos obsoletos detectados. Limpeza necessaria."
    fi
fi

if [ $lint_status -eq 0 ]; then
    echo "CONFORMIDADE TOTAL: Nenhuma violacao de camada detectada."
    exit 0
else
    echo "VIOLACAO DETECTADA: Alguem tentou cruzar as fronteiras do Core."
    exit 1
fi
