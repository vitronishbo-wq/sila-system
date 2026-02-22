#!/bin/bash
set -euo pipefail

ROOT_DIR="$(pwd)"
MODULES_DIR="apps/backend/modules"
BACKUP_DIR="${ROOT_DIR}/.module_tables_backup_$(date +%Y%m%d_%H%M%S)"
BRANCH_NAME="reorg/tables-$(date +%Y%m%d_%H%M%S)"

echo "1) Criando backup dos ficheiros de módulos em: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cp -r "$MODULES_DIR" "$BACKUP_DIR/"

echo "2) Criando branch git '$BRANCH_NAME'"
git checkout -b "$BRANCH_NAME"

echo "3) Gerando mapeamento e aplicando alterações (via Python helper)"
python3 ./scripts/reorg_tables_apply.py --modules "$MODULES_DIR" --apply

echo "4) Verificação git status:"
git status --porcelain

echo "5) Criando commit temporário"
git add -A "$MODULES_DIR"
git commit -m "reorg: apply __tablename__ normalization (automated)" || echo "⚠️ nothing to commit"

PATCH_FILE="${ROOT_DIR}/patches/reorg_tablenames_$(date +%Y%m%d_%H%M%S).patch"
mkdir -p patches
git format-patch -1 --stdout > "$PATCH_FILE"
echo "Patch saved to: $PATCH_FILE"

echo "Relatório final em: ${ROOT_DIR}/reorg_report.json"
