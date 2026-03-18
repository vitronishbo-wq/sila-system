#!/usr/bin/env python3
"""Seed institucional inicial para educacao (Angola).

Inclui:
- anos letivos (setembro-junho)
- escolas com codigo MED
- turmas base por escola/ano
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import date
from pathlib import Path
import sys
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.modules.educacao.infrastructure.models import (
    AnoLetivoModel,
    EscolaModel,
    TurmaModel,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.models.attachment_model import (  # noqa: F401
    AttachmentModel,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.models.request_event_model import (  # noqa: F401
    RequestEventModel,
)


ANOS = [
    {
        "id": UUID("e5047a40-cd8a-4e40-bfdd-467f76d467bb"),
        "ano": 2025,
        "data_inicio": date(2025, 9, 1),
        "data_fim": date(2026, 6, 30),
        "ativo": True,
    },
    {
        "id": UUID("36a95d8c-8f7a-4d1b-b5f1-2ec39570ab7f"),
        "ano": 2026,
        "data_inicio": date(2026, 9, 1),
        "data_fim": date(2027, 6, 30),
        "ativo": False,
    },
]

ESCOLAS = [
    {
        "id": UUID("d7668e8f-c6b6-4ad8-a9d8-696c16ea95a6"),
        "codigo_med": "LUA/KAZ/0012",
        "nome": "Escola Primaria 1 de Maio",
        "tipo": "publica",
        "ciclos": ["primario"],
        "provincia": "Luanda",
        "municipio": "Cazenga",
        "comuna": "Hoji-ya-Henda",
        "bairro": "11 de Novembro",
        "endereco": "Rua Principal, Hoji-ya-Henda",
        "contacto": "+244 923 000 120",
        "email": "ep1maio.luanda@med.gov.ao",
        "ativa": True,
    },
    {
        "id": UUID("0a59f4cb-2086-4a7f-809f-65ca08a7a9f9"),
        "codigo_med": "HUA/CBB/0007",
        "nome": "Complexo Escolar 4 de Fevereiro",
        "tipo": "publica",
        "ciclos": ["primario", "secundario_1"],
        "provincia": "Huambo",
        "municipio": "Caala",
        "comuna": "Sede",
        "bairro": "Centro",
        "endereco": "Avenida da Independencia, Caala",
        "contacto": "+244 923 000 707",
        "email": "ce4fevereiro.huambo@med.gov.ao",
        "ativa": True,
    },
    {
        "id": UUID("f5d80d94-8a6f-4f7a-8ef0-f58ecb9b86dc"),
        "codigo_med": "BGU/LOB/0018",
        "nome": "Liceu Nacional de Lobito",
        "tipo": "publico_privada",
        "ciclos": ["secundario_1", "secundario_2", "tecnico"],
        "provincia": "Benguela",
        "municipio": "Lobito",
        "comuna": "Restinga",
        "bairro": "Compao",
        "endereco": "Rua do Porto, Restinga",
        "contacto": "+244 923 000 918",
        "email": "liceu.lobito@med.gov.ao",
        "ativa": True,
    },
]

TURMAS = [
    {
        "id": UUID("0d72a671-e141-4f0b-a07c-93289f86045f"),
        "escola_id": UUID("d7668e8f-c6b6-4ad8-a9d8-696c16ea95a6"),
        "ano_letivo_id": UUID("e5047a40-cd8a-4e40-bfdd-467f76d467bb"),
        "codigo": "1A",
        "classe": "1a",
        "turno": "manha",
        "capacidade": 45,
        "ativa": True,
    },
    {
        "id": UUID("9a15b238-ecf8-4857-81cb-e53405695f8a"),
        "escola_id": UUID("d7668e8f-c6b6-4ad8-a9d8-696c16ea95a6"),
        "ano_letivo_id": UUID("e5047a40-cd8a-4e40-bfdd-467f76d467bb"),
        "codigo": "5A",
        "classe": "5a",
        "turno": "tarde",
        "capacidade": 45,
        "ativa": True,
    },
    {
        "id": UUID("9dd7ebad-d831-4f48-b177-6f2f6d87d0f7"),
        "escola_id": UUID("0a59f4cb-2086-4a7f-809f-65ca08a7a9f9"),
        "ano_letivo_id": UUID("e5047a40-cd8a-4e40-bfdd-467f76d467bb"),
        "codigo": "7A",
        "classe": "7a",
        "turno": "manha",
        "capacidade": 40,
        "ativa": True,
    },
    {
        "id": UUID("e2f67dc3-8552-4b61-9256-10c08986cc22"),
        "escola_id": UUID("0a59f4cb-2086-4a7f-809f-65ca08a7a9f9"),
        "ano_letivo_id": UUID("e5047a40-cd8a-4e40-bfdd-467f76d467bb"),
        "codigo": "9B",
        "classe": "9a",
        "turno": "tarde",
        "capacidade": 40,
        "ativa": True,
    },
    {
        "id": UUID("e48736e4-f219-4cb6-b85d-4308bcbca04f"),
        "escola_id": UUID("f5d80d94-8a6f-4f7a-8ef0-f58ecb9b86dc"),
        "ano_letivo_id": UUID("e5047a40-cd8a-4e40-bfdd-467f76d467bb"),
        "codigo": "10A",
        "classe": "10a",
        "turno": "manha",
        "capacidade": 35,
        "ativa": True,
    },
    {
        "id": UUID("1072e2bd-5688-472f-95ad-f3017f945ab7"),
        "escola_id": UUID("f5d80d94-8a6f-4f7a-8ef0-f58ecb9b86dc"),
        "ano_letivo_id": UUID("e5047a40-cd8a-4e40-bfdd-467f76d467bb"),
        "codigo": "12T",
        "classe": "12a",
        "turno": "noite",
        "capacidade": 30,
        "ativa": True,
    },
]


async def seed(dry_run: bool) -> dict[str, int]:
    created = {"anos": 0, "escolas": 0, "turmas": 0}
    updated = {"anos": 0, "escolas": 0, "turmas": 0}

    async with AsyncSessionLocal() as session:
        try:
            for item in ANOS:
                row = (
                    await session.execute(select(AnoLetivoModel).where(AnoLetivoModel.ano == item["ano"]))
                ).scalars().first()
                if row:
                    row.data_inicio = item["data_inicio"]
                    row.data_fim = item["data_fim"]
                    row.ativo = item["ativo"]
                    updated["anos"] += 1
                else:
                    session.add(AnoLetivoModel(**item))
                    created["anos"] += 1

            for item in ESCOLAS:
                row = (
                    await session.execute(
                        select(EscolaModel).where(EscolaModel.codigo_med == item["codigo_med"])
                    )
                ).scalars().first()
                if row:
                    for key, value in item.items():
                        setattr(row, key, value)
                    updated["escolas"] += 1
                else:
                    session.add(EscolaModel(**item))
                    created["escolas"] += 1

            for item in TURMAS:
                row = (
                    await session.execute(
                        select(TurmaModel).where(
                            TurmaModel.escola_id == item["escola_id"],
                            TurmaModel.ano_letivo_id == item["ano_letivo_id"],
                            TurmaModel.codigo == item["codigo"],
                        )
                    )
                ).scalars().first()
                if row:
                    for key, value in item.items():
                        setattr(row, key, value)
                    updated["turmas"] += 1
                else:
                    session.add(TurmaModel(**item))
                    created["turmas"] += 1
        except ProgrammingError as exc:
            msg = str(exc).lower()
            if "relation" in msg and "educacao_" in msg:
                raise RuntimeError(
                    "Tabelas de educacao nao encontradas. Execute `alembic upgrade head` primeiro."
                ) from exc
            raise

        if dry_run:
            await session.rollback()
        else:
            await session.commit()

    return {
        "created_anos": created["anos"],
        "updated_anos": updated["anos"],
        "created_escolas": created["escolas"],
        "updated_escolas": updated["escolas"],
        "created_turmas": created["turmas"],
        "updated_turmas": updated["turmas"],
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed institucional de educacao (Angola).")
    parser.add_argument("--dry-run", action="store_true", help="Executa sem commit.")
    return parser.parse_args()


async def _main() -> None:
    args = _parse_args()
    result = await seed(dry_run=args.dry_run)
    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(
        f"[{mode}] "
        f"anos(c={result['created_anos']},u={result['updated_anos']}), "
        f"escolas(c={result['created_escolas']},u={result['updated_escolas']}), "
        f"turmas(c={result['created_turmas']},u={result['updated_turmas']})"
    )


if __name__ == "__main__":
    asyncio.run(_main())
