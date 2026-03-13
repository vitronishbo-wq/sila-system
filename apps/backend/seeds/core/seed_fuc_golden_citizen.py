#!/usr/bin/env python3
"""
⚠️ GOLDEN DEV CITIZEN – FUC (CANONICAL SEED)

🔐 O ÚNICO cidadão hardcode do sistema, exclusivamente para DEV/QA.
Todos os outros cidadãos devem ser criados dinamicamente.

Arquitetura:
✅ Event Sourcing puro (FUC)
✅ Projeções via CitizenProjector.apply_event()
✅ IAM ligado por citizen_id FK
✅ Sem duplicatas, sem gambiarras, sem adaptações

⚠️ NÃO DUPLICAR
⚠️ NÃO ALTERAR SEM RFC
⚠️ NÃO USAR EM PRODUÇÃO (sem credential rotation)
"""

import logging
from uuid import UUID, uuid4
from datetime import date
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup: Adiciona o root do backend ao path para imports de 'app.*'
backend_root = Path(__file__).resolve().parent.parent.parent
# PYTHONPATH should be configured via setup_dev_env.sh; do not mutate sys.path here.

from app.core.settings import settings
from app.core.security import get_password_hash
from app.core.constants import UserRole, AdminLevel
from apps.backend.app.modules.identity.models.user import User

from apps.backend.app.modules.justice.civil_registry.events.models import CitizenEventModel, EventType
from apps.backend.app.modules.justice.civil_registry.projections.projectors import CitizenProjector

# ════════════════════════════════════════════════════════════════════
# 🏛️ IDENTIDADE FIXA (CANÓNICA) — O ÚNICO HARDCODE PERMITIDO
# ════════════════════════════════════════════════════════════════════

GOLDEN_CITIZEN_ID = UUID("11111111-1983-05-01-0000-000000000001")

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


def seed_golden_citizen():
    """Cria o cidadão de referência (GOLDEN RECORD) via Event Sourcing puro."""

    # Converter DATABASE_URL async para sync
    sync_database_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_database_url, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    
    db = SessionLocal()
    logger.info("🌟 Criando GOLDEN DEV CITIZEN (FUC)...")

    try:
        projector = CitizenProjector(db)

        # 1️⃣ BIRTH_REGISTRATION — Ponto de verdade
        birth_event = CitizenEventModel(
            id=uuid4(),
            citizen_id=GOLDEN_CITIZEN_ID,
            event_type=EventType.BIRTH_REGISTRATION,
            payload={
                "full_name": FULL_NAME,
                "birth_date": BIRTH_DATE.isoformat(),
                "gender": GENDER,
                "nationality": NATIONALITY,
                "place_of_birth": PLACE_OF_BIRTH,
                "father_name": FATHER_NAME,
                "mother_name": MOTHER_NAME,
            },
            legal_basis="Lei do Registo Civil (GOLDEN SEED)",
            service_id="SEED_GOLDEN_CITIZEN",
            performed_by="SYSTEM",
        )
        db.add(birth_event)
        db.flush()
        projector.apply_event(birth_event)
        logger.info("   ✅ BIRTH_REGISTRATION → Projeção de nascimento")

        # 2️⃣ VITAL_STATUS_CHANGE — Estado de vida
        vital_event = CitizenEventModel(
            id=uuid4(),
            citizen_id=GOLDEN_CITIZEN_ID,
            event_type=EventType.VITAL_STATUS_CHANGE,
            payload={"status": "ALIVE"},
            legal_basis="Declaração de Vida (SEED)",
            service_id="SEED_GOLDEN_CITIZEN",
            performed_by="SYSTEM",
        )
        db.add(vital_event)
        db.flush()
        projector.apply_event(vital_event)
        logger.info("   ✅ VITAL_STATUS_CHANGE → Cidadão vivo")

        # 3️⃣ ADDRESS_UPDATE — Morada
        address_event = CitizenEventModel(
            id=uuid4(),
            citizen_id=GOLDEN_CITIZEN_ID,
            event_type=EventType.ADDRESS_UPDATE,
            payload=ADDRESS,
            legal_basis="Declaração de Residência (SEED)",
            service_id="SEED_GOLDEN_CITIZEN",
            performed_by="SYSTEM",
        )
        db.add(address_event)
        db.flush()
        projector.apply_event(address_event)
        logger.info("   ✅ ADDRESS_UPDATE → Morada registada")

        # 4️⃣ ID_CARD_ISSUED — Bilhete de Identidade
        bi_event = CitizenEventModel(
            id=uuid4(),
            citizen_id=GOLDEN_CITIZEN_ID,
            event_type=EventType.ID_CARD_ISSUED,
            payload={
                "card_id": BI_NUMBER,
                "issued_at": BI_ISSUED_AT.isoformat(),
                "expires_at": BI_EXPIRES_AT.isoformat(),
                "issuing_authority": BI_AUTHORITY,
            },
            legal_basis="Emissão de BI (SEED)",
            service_id="SEED_GOLDEN_CITIZEN",
            performed_by="SYSTEM",
        )
        db.add(bi_event)
        db.flush()
        projector.apply_event(bi_event)
        logger.info("   ✅ ID_CARD_ISSUED → BI registado")

        # 5️⃣ USER IAM — Credenciais para login no portal
        user = User(
            id=uuid4(),
            email=EMAIL,
            username="truman.sapalo",
            password_hash=get_password_hash(PASSWORD),
            role=UserRole.CITIZEN.value,           # ✅ Enum
            level=AdminLevel.CITIZEN.value,        # ✅ Enum
            citizen_id=GOLDEN_CITIZEN_ID,          # ✅ FK explícito
            is_active=True,
            territory_id=None,                     # Cidadão sem restrição territorial
        )
        db.add(user)
        logger.info("   ✅ USER IAM → Credenciais criadas")

        # 6️⃣ COMMIT final
        db.commit()
        logger.info("✅ Transação completa com sucesso!")

        # 7️⃣ Output humano
        print("\n" + "="*70)
        print("🌟 GOLDEN DEV CITIZEN CRIADO COM SUCESSO")
        print("="*70)
        print(f"\n📋 IDENTIDADE:")
        print(f"   Nome: {FULL_NAME}")
        print(f"   Data Nasc: {BIRTH_DATE.strftime('%d/%m/%Y')}")
        print(f"   Género: {GENDER}")
        print(f"   Nacionalidade: {NATIONALITY}")
        print(f"   BI: {BI_NUMBER}")
        print(f"   Pai: {FATHER_NAME}")
        print(f"   Mãe: {MOTHER_NAME}")
        
        print(f"\n📍 MORADA:")
        print(f"   Residência: {ADDRESS['residence']}")
        print(f"   Localização: {ADDRESS['quadra']}/{ADDRESS['predio']}")
        print(f"   Comuna: {ADDRESS['comuna']}, {ADDRESS['municipio']}")
        print(f"   Província: {ADDRESS['provincia']}")
        
        print(f"\n🔐 CREDENCIAIS DE LOGIN:")
        print(f"   Email: {EMAIL}")
        print(f"   Senha: {PASSWORD}")
        
        print(f"\n🆔 IDENTIFICADORES:")
        print(f"   Citizen ID: {GOLDEN_CITIZEN_ID}")
        print(f"   Role: {UserRole.CITIZEN.value}")
        print(f"   Level: {AdminLevel.CITIZEN.value}")
        
        print(f"\n✅ EVENTOS CRIADOS:")
        print(f"   1. BIRTH_REGISTRATION")
        print(f"   2. VITAL_STATUS_CHANGE")
        print(f"   3. ADDRESS_UPDATE")
        print(f"   4. ID_CARD_ISSUED")
        
        print("\n" + "="*70)
        print("🎯 Este é o GOLDEN RECORD do SILA")
        print("   → Todos os módulos podem usar este cidadão")
        print("   → Qualquer bug é reproduzível")
        print("   → Event Sourcing respeitado 100%")
        print("="*70 + "\n")

        return {
            "citizen_id": str(GOLDEN_CITIZEN_ID),
            "email": EMAIL,
            "password": PASSWORD,
            "full_name": FULL_NAME,
            "status": "✅ GOLDEN RECORD CRIADO",
        }

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao criar GOLDEN CITIZEN: {e}", exc_info=True)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s"
    )
    result = seed_golden_citizen()
    print("✅ GOLDEN CITIZEN seed completado!")
