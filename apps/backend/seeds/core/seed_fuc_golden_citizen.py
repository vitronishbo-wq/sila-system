#!/usr/bin/env python3
"""
ATENCAO: GOLDEN DEV CITIZEN – FUC (CANONICAL SEED)

O UNICO cidadao hardcode do sistema, exclusivamente para DEV/QA.
Todos os outros cidadãos devem ser criados dinamicamente.

Arquitetura (atual):
- Repositorio canonico (IdentityCitizenRepository)
- Modelo real (CitizenFUC)
- Sem inserts diretos (sem SQL manual)
- Idempotente (create/update)

NAO DUPLICAR
NAO ALTERAR SEM RFC
NAO USAR EM PRODUCAO (sem credential rotation)
"""

import asyncio
import logging
import os
from datetime import date
from uuid import UUID

from apps.backend.app.core.bridges.identity_bridge import CitizenFUC, IdentityCitizenRepository
from apps.backend.app.core.db import db
from sqlalchemy import select

# ════════════════════════════════════════════════════════════════════
# IDENTIDADE FIXA (CANONICA) — O UNICO HARDCODE PERMITIDO
# ════════════════════════════════════════════════════════════════════

GOLDEN_CITIZEN_ID = UUID("11111111-1983-0501-0000-000000000001")

EMAIL = "truman@gmail.com"
PASSWORD = "Sila_1983"

FULL_NAME = "Truman José Sapalo"
BIRTH_DATE = date(1983, 5, 1)
GENDER = "M"
NATIONALITY = "Angolana"

FATHER_NAME = "José Sapalo"
MOTHER_NAME = "Maria de Lourdes"

HEIGHT = 1.80
MARITAL_STATUS = "SINGLE"

BI_NUMBER = "001508576HO034"
BI_ISSUED_AT = date(2021, 7, 23)
BI_EXPIRES_AT = date(2031, 7, 22)
BI_AUTHORITY = "Arquivo de Identificação de Huambo"

ADDRESS = {
    "residence": "Centralidade do Lossambo",
    "quadra": "18",
    "predio": "15",
    "apartamento": "1.2",
    "comuna": "Huambo",
    "municipio": "Huambo",
    "provincia": "Huambo",
    "pais": "Angola",
}

PLACE_OF_BIRTH = {
    "bairro": "Chianga",
    "comuna": "Huambo",
    "municipio": "Huambo",
    "provincia": "Huambo",
    "pais": "Angola",
}

# ════════════════════════════════════════════════════════════════════

logger = logging.getLogger(__name__)

CRITICAL_FIELDS = {"full_name", "birth_date", "document_number"}


def _collect_differences(existing: CitizenFUC) -> list[tuple[str, object, object]]:
    """Collect field-level differences between existing record and golden seed."""
    expected = {
        "full_name": FULL_NAME,
        "email": EMAIL,
        "birth_date": BIRTH_DATE,
        "document_number": BI_NUMBER,
        "vital_status": "alive",
    }

    if os.getenv("GOLDEN_CITIZEN_FORCE_DIVERGENCE"):
        expected["full_name"] = f"{FULL_NAME} (DIVERGENCE_TEST)"

    differences: list[tuple[str, object, object]] = []
    for field, expected_value in expected.items():
        current_value = getattr(existing, field, None)
        if current_value != expected_value:
            differences.append((field, current_value, expected_value))
    return differences


def _log_field_differences(differences: list[tuple[str, object, object]]) -> None:
    if not differences:
        return
    logger.warning("Golden citizen divergences detected:")
    for field, current_value, expected_value in differences:
        logger.warning(
            " - %s: current=%s expected=%s",
            field,
            current_value,
            expected_value,
        )


def _has_critical_differences(differences: list[tuple[str, object, object]]) -> bool:
    return any(field in CRITICAL_FIELDS for field, _, _ in differences)


async def seed_golden_citizen():
    """Cria/atualiza o cidadão de referência (GOLDEN RECORD) via módulos reais."""
    logger.info("Criando GOLDEN DEV CITIZEN (FUC)...")

    try:
        async with db.transaction() as session:
            repo = IdentityCitizenRepository(session)

            existing = await repo.get_by_id(GOLDEN_CITIZEN_ID)
            if not existing:
                result = await session.execute(
                    select(CitizenFUC).where(CitizenFUC.document_number == BI_NUMBER)
                )
                existing = result.scalar_one_or_none()

            if existing:
                differences = _collect_differences(existing)
                _log_field_differences(differences)
                strict_mode = os.getenv("GOLDEN_CITIZEN_STRICT", "1") != "0"
                if strict_mode and _has_critical_differences(differences):
                    raise ValueError("Critical divergences found in GOLDEN citizen record.")
                existing.full_name = FULL_NAME
                existing.email = EMAIL
                existing.birth_date = BIRTH_DATE
                existing.document_number = BI_NUMBER
                existing.vital_status = "alive"
                await repo.update(existing, commit=False)
                action = "atualizado"
            else:
                citizen = CitizenFUC(
                    citizen_id=GOLDEN_CITIZEN_ID,
                    full_name=FULL_NAME,
                    email=EMAIL,
                    birth_date=BIRTH_DATE,
                    document_number=BI_NUMBER,
                    vital_status="alive",
                )
                await repo.create(citizen, commit=False)
                action = "criado"

            # Output humano
            print("\n" + "=" * 70)
            print(f"GOLDEN DEV CITIZEN {action.upper()} COM SUCESSO")
            print("=" * 70)
            print("\nIDENTIDADE:")
            print(f"   Nome: {FULL_NAME}")
            print(f"   Data Nasc: {BIRTH_DATE.strftime('%d/%m/%Y')}")
            print(f"   Género: {GENDER}")
            print(f"   Nacionalidade: {NATIONALITY}")
            print(f"   BI: {BI_NUMBER}")
            print(f"   Pai: {FATHER_NAME}")
            print(f"   Mãe: {MOTHER_NAME}")

            print("\nMORADA:")
            print(f"   Residência: {ADDRESS['residence']}")
            print(f"   Localização: {ADDRESS['quadra']}/{ADDRESS['predio']}")
            print(f"   Comuna: {ADDRESS['comuna']}, {ADDRESS['municipio']}")
            print(f"   Província: {ADDRESS['provincia']}")
            print("   Nota: morada e dados detalhados são informativos no seed.")

            print("\nCREDENCIAIS DE LOGIN:")
            print(f"   Email: {EMAIL}")
            print(f"   Senha: {PASSWORD}")

            print("\nIDENTIFICADORES:")
            print(f"   Citizen ID: {GOLDEN_CITIZEN_ID}")

            print("\n" + "=" * 70)
            print("Este e o GOLDEN RECORD do SILA")
            print("   -> Todos os modulos podem usar este cidadao")
            print("   -> Qualquer bug e reproduzivel")
            print("   -> Seed alinhado aos modulos reais (FUC)")
            print("=" * 70 + "\n")

            return {
                "citizen_id": str(GOLDEN_CITIZEN_ID),
                "email": EMAIL,
                "password": PASSWORD,
                "full_name": FULL_NAME,
                "status": f"✅ GOLDEN RECORD {action.upper()}",
            }
    except Exception as exc:
        logger.error(f"Erro ao criar GOLDEN CITIZEN: {exc}", exc_info=True)
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    result = asyncio.run(seed_golden_citizen())
    print("GOLDEN CITIZEN seed completado!")
