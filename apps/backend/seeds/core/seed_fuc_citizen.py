#!/usr/bin/env python3
"""
⚠️ DEPRECATED — Use seed_fuc_golden_citizen.py em vez disso

🔐 SEED CANÓNICA DEV — Criar Cidadão Funcional Completo no FUC

STATUS: ⚠️ SUBSTITUÍDO POR seed_fuc_golden_citizen.py
- Script anterior mantido para compatibilidade
- Use o GOLDEN CITIZEN script para novos cidadãos padrão

Cria:
1. Evento FUC (BIRTH_REGISTRATION) — ponto de verdade
2. Projeção cidadão via CitizenProjector.apply_event() — respeitando Event Sourcing
3. Usuário FUC para login com citizen_id FK — vínculo explícito
4. Usa enums próprios (UserRole.CITIZEN, AdminLevel.CITIZEN) — sem hardcoding

Uso:
    python -m seeds.core.seed_fuc_citizen
    
Arquitetura (PADRÃO CANÓNICO):
    Event → flush() → CitizenProjector.apply_event() → Projection + Commit
    User(citizen_id, role=UserRole.CITIZEN.value, level=AdminLevel.CITIZEN.value)

Validações de Conformidade:
    ✅ Ponto 1: Projeção NÃO é criada manualmente (usa CitizenProjector)
    ✅ Ponto 2: Vínculo User ↔ Citizen via citizen_id FK
    ✅ Ponto 3: Roles e levels vêm de enums (UserRole, AdminLevel)
"""

# ⚠️ ╔════════════════════════════════════════════════════════════╗
# ⚠️ ║    CANONICAL DEV SEED – FUC                               ║
# ⚠️ ║    🚫 NÃO DUPLICAR                                        ║
# ⚠️ ║    🚫 NÃO ADAPTAR                                         ║
# ⚠️ ║    🚫 NÃO USAR EM PROD (sem credential rotation)          ║
# ⚠️ ╚════════════════════════════════════════════════════════════╝

import logging
import uuid
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings
from app.core.security import get_password_hash
from app.core.constants import UserRole, AdminLevel
from modules.identity.models.user import User
from app.modules.justice.civil_registry.events.models import CitizenEventModel, EventType
from app.modules.justice.civil_registry.projections.projectors import CitizenProjector

logger = logging.getLogger(__name__)

# ==================== DADOS DO CIDADÃO ====================
CITIZEN_FULL_NAME = "Ana Silva Cidadão"
CITIZEN_EMAIL = "ana.silva@cidadao.ang"
CITIZEN_PASSWORD = "Cidadao_1983"
CITIZEN_BIRTH_DATE = date(1988, 7, 22)
CITIZEN_GENDER = "F"
CITIZEN_BI = "000123456BI001"
CITIZEN_NIF = "123456789AB001"

def seed_fuc_citizen():
    """Cria cidadão completo no FUC respeitando Event Sourcing + IAM design"""
    
    # Converter DATABASE_URL async para sync (remover +asyncpg)
    sync_database_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_database_url, echo=False)
    SessionLocal = sessionmaker(bind=engine)
    
    db = SessionLocal()
    logger.info("🌱 Iniciando seed de cidadão FUC...")
    
    try:
        # 1️⃣ Gerar IDs únicos
        citizen_id = uuid.uuid4()
        event_id = uuid.uuid4()
        user_id = uuid.uuid4()
        
        logger.info(f"   Citizen ID: {citizen_id}")
        logger.info(f"   Event ID: {event_id}")
        logger.info(f"   User ID: {user_id}")
        
        # 2️⃣ Criar evento FUC (EVENT SOURCING)
        # ✅ Ponto 1: Criar evento é o ponto de verdade
        birth_event = CitizenEventModel(
            id=event_id,
            citizen_id=citizen_id,
            event_type=EventType.BIRTH_REGISTRATION,
            payload={
                "full_name": CITIZEN_FULL_NAME,
                "birth_date": CITIZEN_BIRTH_DATE.isoformat(),
                "gender": CITIZEN_GENDER,
                "nationality": "Angolana",
                "bi_number": CITIZEN_BI,
                "nif": CITIZEN_NIF,
            },
            legal_basis="Lei de Registo Civil - Decreto 03/22 (SEED)",
            service_id="SEED_FUC_CITIZEN_001",
            performed_by="SYSTEM"
        )
        db.add(birth_event)
        db.flush()  # Garante que ID foi atribuído
        logger.info(f"   ✅ Evento BIRTH_REGISTRATION criado (via Event Sourcing)")
        
        # 3️⃣ Aplicar evento à projeção via CitizenProjector
        # ✅ Ponto 1: NÃO criar manualmente a projeção, usar projector
        projector = CitizenProjector(db)
        projector.apply_event(birth_event)
        logger.info(f"   ✅ Projeção cidadão criada via CitizenProjector.apply_event()")
        
        # 4️⃣ Criar usuário FUC (para login no portal)
        # ✅ Ponto 2: Linkar ao cidadão via citizen_id FK
        # ✅ Ponto 3: Usar enums propriamente (UserRole.CITIZEN, AdminLevel.CITIZEN)
        citizen_user = User(
            id=user_id,
            email=CITIZEN_EMAIL,
            username=f"cidadao_{citizen_id.hex[:8]}",
            password_hash=get_password_hash(CITIZEN_PASSWORD),
            role=UserRole.CITIZEN.value,      # ✅ Enum, not hardcoded string
            level=AdminLevel.CITIZEN.value,   # ✅ Enum, not hardcoded string
            is_active=True,
            citizen_id=citizen_id,            # ✅ FK ao cidadão no FUC (PONTO 2)
            territory_id=None,                # Cidadão não tem restrição territorial
        )
        db.add(citizen_user)
        logger.info(f"   ✅ Usuário FUC criado (citizen_id linkado + enums)")
        
        # 5️⃣ Commit transação completa
        db.commit()
        logger.info("   ✅ Commit realizado com sucesso!")
        
        # 6️⃣ Print credenciais
        print("\n" + "="*70)
        print("🎉 CIDADÃO FUC CRIADO COM SUCESSO!")
        print("="*70)
        print(f"\n📋 DADOS DO CIDADÃO:")
        print(f"   Nome: {CITIZEN_FULL_NAME}")
        print(f"   Citizen ID: {citizen_id}")
        print(f"   Data Nasc: {CITIZEN_BIRTH_DATE}")
        print(f"   Género: {CITIZEN_GENDER}")
        print(f"   BI: {CITIZEN_BI}")
        print(f"   NIF: {CITIZEN_NIF}")
        
        print(f"\n🔐 CREDENCIAIS DE LOGIN:")
        print(f"   Email: {CITIZEN_EMAIL}")
        print(f"   Senha: {CITIZEN_PASSWORD}")
        print(f"   User ID: {user_id}")
        
        print(f"\n🔗 RELACIONAMENTOS:")
        print(f"   Evento Criador: {event_id}")
        print(f"   User → Citizen FK: {citizen_id}")
        print(f"   Role: {UserRole.CITIZEN.value}")
        print(f"   Level: {AdminLevel.CITIZEN.value}")
        
        print("\n" + "="*70)
        print("✅ Padrão de arquitetura:")
        print("   → Event Sourcing: ✅ CitizenProjector.apply_event()")
        print("   → IAM Linkage: ✅ User.citizen_id FK → citizen_fuc")
        print("   → Enums: ✅ UserRole.CITIZEN + AdminLevel.CITIZEN")
        print("="*70 + "\n")
        
        return {
            "citizen_id": str(citizen_id),
            "user_id": str(user_id),
            "email": CITIZEN_EMAIL,
            "password": CITIZEN_PASSWORD,
            "full_name": CITIZEN_FULL_NAME,
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao criar cidadão: {e}", exc_info=True)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    result = seed_fuc_citizen()
    print("✅ Seed completado com sucesso!")
