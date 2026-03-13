#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="apps/backend/app/modules"
DRY_RUN=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --root)
            ROOT_DIR="${2:-}"
            shift 2
            ;;
        *)
            echo "Uso: $0 [--dry-run] [--root <path>]"
            exit 1
            ;;
    esac
done

if [[ -z "${ROOT_DIR}" || ! -d "${ROOT_DIR}" ]]; then
    echo "Diretorio invalido: ${ROOT_DIR}"
    exit 1
fi

python3 - "${ROOT_DIR}" "${DRY_RUN}" <<'PY'
from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1])
dry_run = bool(int(sys.argv[2]))

replacements = [
    ("app.modules.infrastructure_sector.transportes_logistica", "app.modules.infrastructure_sector.logistica.transport"),
    ("app.modules.infrastructure_sector.portos_logistica", "app.modules.infrastructure_sector.logistica.ports"),
    ("app.modules.resources.pescas_industriais", "app.modules.resources.pescas.industrial"),
    ("app.modules.economy.financas_publicas", "app.modules.economy.financas.public_budget"),
    ("app.modules.economy.financas_impostos", "app.modules.economy.financas.taxation"),
    ("app.modules.economy.comercio_servicos", "app.modules.economy.trade.services"),
    ("app.modules.economy.comercio_externo", "app.modules.economy.trade.external"),
    ("apps/backend/app/modules/infrastructure_sector/transportes_logistica", "apps/backend/app/modules/infrastructure_sector/logistica/transport"),
    ("apps/backend/app/modules/infrastructure_sector/portos_logistica", "apps/backend/app/modules/infrastructure_sector/logistica/ports"),
    ("apps/backend/app/modules/resources/pescas_industriais", "apps/backend/app/modules/resources/pescas/industrial"),
    ("apps/backend/app/modules/economy/financas_publicas", "apps/backend/app/modules/economy/financas/public_budget"),
    ("apps/backend/app/modules/economy/financas_impostos", "apps/backend/app/modules/economy/financas/taxation"),
    ("apps/backend/app/modules/economy/comercio_servicos", "apps/backend/app/modules/economy/trade/services"),
    ("apps/backend/app/modules/economy/comercio_externo", "apps/backend/app/modules/economy/trade/external"),
]

extensions = {
    ".py", ".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".sql", ".sh",
}
skip_dirs = {"__pycache__", ".git", "node_modules", ".venv"}

counts = {old: 0 for old, _new in replacements}
changed_files: list[str] = []
scanned = 0

for path in root.rglob("*"):
    if not path.is_file():
        continue
    if any(part in skip_dirs for part in path.parts):
        continue
    if path.suffix not in extensions:
        continue

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue

    scanned += 1
    new_text = text
    file_changed = False

    for old, new in replacements:
        n = new_text.count(old)
        if n:
            counts[old] += n
            new_text = new_text.replace(old, new)
            file_changed = True

    if file_changed:
        changed_files.append(path.as_posix())
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")

print(f"mode={'dry-run' if dry_run else 'apply'}")
print(f"root={root.as_posix()}")
print(f"scanned_files={scanned}")
print(f"changed_files={len(changed_files)}")
for old, _new in replacements:
    if counts[old]:
        print(f"{old} -> {counts[old]}")

if changed_files:
    print("sample_changed_files:")
    for item in changed_files[:20]:
        print(item)
PY
