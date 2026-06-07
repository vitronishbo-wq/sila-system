#!/usr/bin/env python3
"""Generate defesa_consumidor structure placeholders."""

from __future__ import annotations

from pathlib import Path

BASE = Path("apps/backend/app/modules/defesa_consumidor")
FILES = [
    "api/router.py",
    "api/deps.py",
    "api/endpoints/reclamacoes.py",
    "api/schemas/reclamacao_schema.py",
    "application/services/reclamacao_service.py",
    "domain/models/reclamacao.py",
    "infrastructure/repositories/sqlalchemy_reclamacao_repository.py",
    "tests/test_reclamacoes.py",
]


def main() -> None:
    for rel in FILES:
        target = BASE / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(f"'''placeholder {rel}'''\n", encoding="utf-8")
            print(f"created {target}")
    print("done")


if __name__ == "__main__":
    main()
