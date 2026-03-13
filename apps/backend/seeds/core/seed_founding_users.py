"""
Seed script para os 4 users fundadores de SILA

Padrão RBAC territorial:
- central@sila.gov.ao    → ADMIN_CENTRAL (acesso nacional)
- prov.huambo@sila.gov.ao → ADMIN_PROVINCIAL (Huambo)
- mun.huambo@sila.gov.ao → ADMIN_MUNICIPAL (Huambo cidade)
- comun.huambo@sila.gov.ao → ADMIN_COMMUNAL (comunas de Huambo)

Senha universal: Sila_1983
"""

import asyncio
import logging
from uuid import uuid4
from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.core.security import get_password_hash
from apps.backend.app.modules.identity.models.user import User
from app.core.territory.models.territory import Territory
from app.core.constants import UserRole, ROLE_TO_LEVEL

logger = logging.getLogger(__name__)

# ==================== USERS CONFIG ====================
FOUNDING_USERS = [
    {
        "email": "central@sila.gov.ao",
        "username": "central_admin",
        "role": UserRole.ADMIN_CENTRAL,
        "territory_id": None,  # Sem restrição territorial
    },
    {
        "email": "prov.huambo@sila.gov.ao",
        "username": "prov_huambo",
        "role": UserRole.ADMIN_PROVINCIAL,
        "territory_code": "HUA",  # Será resolvido ao Huambo
    },
    {
        "email": "mun.huambo@sila.gov.ao",
        "username": "mun_huambo",
        "role": UserRole.ADMIN_MUNICIPAL,
        "territory_code": "HUA-HUA",  # Huambo (municipalidade)
    },
    {
        "email": "comun.huambo@sila.gov.ao",
        "username": "comun_huambo",
        "role": UserRole.ADMIN_COMMUNAL,
        "territory_code": "HUA-HUA-*",  # Qualquer comuna sob Huambo
    },
]

UNIVERSAL_PASSWORD = "Sila_1983"


async def seed_founding_users():
    """Seed dos 4 users fundadores com suas roles territoriais"""
    
    async with AsyncSessionLocal() as db:
        logger.info("🌱 Iniciando seed dos users fundadores...")
        
        for user_config in FOUNDING_USERS:
            try:
                # Verificar se user já existe
                query = select(User).where(User.email == user_config["email"])
                existing = await db.execute(query)
                if existing.scalar():
                    logger.info(f"⏭️  {user_config['email']} já existe, pulando...")
                    continue
                
                # Resolver territory se necessário
                territory_id = user_config.get("territory_id")
                if "territory_code" in user_config:
                    territory_query = select(Territory).where(
                        Territory.code == user_config["territory_code"]
                    )
                    territory_result = await db.execute(territory_query)
                    territory = territory_result.scalar()
                    if territory:
                        territory_id = territory.id
                    else:
                        logger.warning(f"⚠️  Território {user_config['territory_code']} não encontrado para {user_config['email']}")
                
                # Derivar level do role
                role_enum = user_config["role"]
                level = ROLE_TO_LEVEL.get(role_enum, "central").value
                
                # Criar user
                user = User(
                    id=uuid4(),
                    email=user_config["email"],
                    username=user_config["username"],
                    password_hash=get_password_hash(UNIVERSAL_PASSWORD),
                    role=role_enum.value,
                    level=level,
                    is_active=True,
                    territory_id=territory_id,
                )
                
                db.add(user)
                logger.info(f"✅ {user_config['email']} ({role_enum.value}) criado")
            
            except Exception as e:
                logger.error(f"❌ Erro ao criar {user_config['email']}: {e}")
        
        try:
            await db.commit()
            logger.info("✅ Users fundadores seed completo!")
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ Erro ao fazer commit: {e}")


async def main():
    """Entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    await seed_founding_users()


if __name__ == "__main__":
    asyncio.run(main())
