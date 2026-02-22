#!/usr/bin/env python3
"""
Script para aplicar (ou dry-run) o patch __table_args__ = {'extend_existing': True} na classe Alert.
Cria backup .bak antes de modificar.
Uso:
  python tools/apply_extend_existing.py --apply   # aplica de fato
  python tools/apply_extend_existing.py           # dry-run (default)
"""
import sys
from pathlib import Path

ALERT_FILE = Path("/opt/sila-system/backend/modules/monitoring/models/alert.py")
PATCH_LINE = "    __table_args__ = {'extend_existing': True}"
APPLY = "--apply" in sys.argv


def patch_alert_file(apply=False):
    if not ALERT_FILE.exists():
        print(f"Arquivo não encontrado: {ALERT_FILE}")
        return False
    text = ALERT_FILE.read_text()
    if "__table_args__" in text:
        print(f"Já existe __table_args__ em {ALERT_FILE}")
        return True
    # injeta logo após a linha 'class Alert(Base):'
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("class Alert(Base):"):
            insert_at = i + 1
            break
    else:
        print("Classe Alert(Base) não encontrada!")
        return False
    if apply:
        # backup
        ALERT_FILE.with_suffix(".py.bak").write_text(text)
        lines.insert(insert_at, PATCH_LINE)
        ALERT_FILE.write_text("\n".join(lines) + "\n")
        print(f"Patch aplicado e backup salvo: {ALERT_FILE}.bak")
    else:
        print("--- DRY RUN ---")
        preview = (
            lines[: insert_at + 1] + ["..."] + lines[insert_at + 1 : insert_at + 4]
        )
        print("\n".join(preview))
        print("Patch seria aplicado acima (use --apply para modificar de fato)")
    return True


if __name__ == "__main__":
    patch_alert_file(apply=APPLY)
