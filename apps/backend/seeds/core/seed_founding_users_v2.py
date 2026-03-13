"""
Seed script para os 4 users fundadores de SILA - VERSÃO CORRIGIDA (2026-02-22)

Padrão RBAC territorial:
- central@sila.gov.ao      → ADMIN_CENTRAL (acesso nacional, region_id=NULL)
- prov.huambo@sila.gov.ao  → ADMIN_PROVINCIAL (Huambo)
- mun.huambo@sila.gov.ao   → ADMIN_MUNICIPAL (Huambo città)
- comun.huambo@sila.gov.ao → ADMIN_COMMUNAL (communes)

Senha universal: Sila_1983

Alinhado com schema real do BD:
- Tabela: users (não iam_users)
- PK: id (INTEGER, auto-increment)
- uuid: VARCHAR (gen_random_uuid)
- email, hashed_password, full_name
- status, is_active, is_verified
- administrative_level, level
- region_id FK → locations.id
- roles: JSON array
"""

import asyncio
import logging
from uuid import uuid4
from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.core.security import get_password_hash
from apps.backend.app.modules.identity.models.user import User

logger = logging.getLogger(__name__)

# ==================== USERS CONFIG ====================
FOUNDING_USERS = [
    {
        "email": "central@sila.gov.ao",
        "full_name": "Administrador Central",
        "administrative_level": "CENTRAL",
        "roles": ["ADMIN", "ADMIN_CENTRAL"],
        "region_id": None,  # Sem restrição territorial (acesso nacional)
    },
    {
        "email": "prov.huambo@sila.gov.ao",
        "full_name": "Administrador Provincial - Huambo",
        "administrative_level": "PROVINCIAL",
        "roles": ["ADMIN", "ADMIN_PROVINCIAL"],
        "region_id": None,  # TODO: Será resolvido ao ID de Huambo após seed de locations
    },
    {
        "email": "mun.huambo@sila.gov.ao",
        "full_name": "Administrador Municipal - Huambo",
        "administrative_level": "MUNICIPAL",
        "roles": ["ADMIN", "ADMIN_MUNICIPAL"],
        "region_id": None,  # TODO: Será resolvido ao ID de Huambo municipality
    },
    {
        "email": "comun.huambo@sila.gov.ao",
        "full_name": "Administrador Comunal - Huambo",
        "administrative_level": "COMMUNAL",
        "roles": ["ADMIN", "ADMIN_COMMUNAL"],
        "region_id": None,  # TODO: Será resolvido ao ID de primeira comuna
    },
    {
        "email": "truman@gmail.com",
        "full_name": "Cidadão Truman",
        "administrative_level": "LOCAL",
        "roles": ["USER", "CITIZEN"],
        "region_id": None,  # Regular citizen
    },
]

UNIVERSAL_PASSWORD = "Test1234"  # Senha curta para testes (< 72 bytes bcrypt limit)


async def seed_founding_users():
    """Seed dos users fundadores com suas roles e níveis administrativos"""
    
    async with AsyncSessionLocal() as db:
        logger.info("=" * 80)
        logger.info("🌱 SEED: Criando users fundadores...")
        logger.info("=" * 80)
        
        created_count = 0
        skipped_count = 0
        
        for user_config in FOUNDING_USERS:
            email = user_config["email"]
            
            try:
                # Verificar se user já existe
                query = select(User).where(User.email == email)
                existing = await db.execute(query)
                if existing.scalar():
                    logger.info(f"⏭️  SKIP: {email} já existe")
                    skipped_count += 1
                    continue
                
                # Criar novo user com campos corretos
                user = User(
                    uuid=str(uuid4()),
                    email=email,
                    hashed_password=get_password_hash(UNIVERSAL_PASSWORD),
                    full_name=user_config.get("full_name", email),
                    phone=None,
                    bi_number=None,
                    
                    # Status fields
                    is_active=True,
                    is_verified=True,
                    status="ACTIVE",
                    
                    # Authorization
                    administrative_level=user_config["administrative_level"],
                    
                    # Geographic
                    region_id=user_config.get("region_id"),
                    
                    # Roles - JSON array
                    roles=user_config.get("roles", ["USER"]),
                )
                
                db.add(user)
                await db.flush()
                
                logger.info(f"✅ CRIADO: {email}")
                logger.info(f"   Level: {user_config['administrative_level']}")
                logger.info(f"   Roles: {user_config.get('roles', [])}")
                
                created_count += 1
                
            except Exception as e:
                logger.error(f"❌ ERRO ao criar {email}: {e}")
        
        # Commit all changes
        await db.commit()
        
        logger.info("\n" + "=" * 80)
        logger.info(f"📊 RESULTADO:")
        logger.info(f"   ✅ Criados: {created_count}")
        logger.info(f"   ⏭️  Pulados: {skipped_count}")
        logger.info("=" * 80)
        
        # Validation
        logger.info("\n" + "=" * 80)
        logger.info("✅ VALIDAÇÃO: Users cadastrados")
        logger.info("=" * 80)
        
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        for user in users:
            logger.info(f"  {user.email:30} | {user.administrative_level:12} | Roles: {user.roles}")
        
        logger.info(f"\n📈 Total: {len(users)} users no banco")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    asyncio.run(seed_founding_users())
