import asyncio
import uuid
import sys
import os
from pathlib import Path
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

# Adiciona o root do backend ao path
backend_root = Path(__file__).resolve().parent.parent.parent
# PYTHONPATH should be configured via setup_dev_env.sh; do not mutate sys.path here.

# Carrega variáveis de ambiente do .env
load_dotenv(backend_root / ".env")

from app.core.settings import settings
from app.core.database import AsyncSessionLocal
from modules.identity.models.user import User
from app.core.territory.models.territory import Territory
from app.core.security import get_password_hash, create_access_token

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "central@sila.gov.ao")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Sila_1983")

async def seed_and_token():
    async with AsyncSessionLocal() as session:
        # Importante: Registrar Territory no metadata antes da query ao User
        # para evitar erros de mapeamento no SQLAlchemy
        result = await session.execute(select(User).where(User.email == ADMIN_EMAIL))
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                id=uuid.uuid4(),
                email=ADMIN_EMAIL,
                username="central",
                password_hash=get_password_hash(ADMIN_PASSWORD),
                level="central",
                role="admin_central",
                is_active=True
            )
            session.add(user)
            await session.commit()
            print(f"✅ Admin criado: {ADMIN_EMAIL}")
        else:
            user.password_hash = get_password_hash(ADMIN_PASSWORD)
            await session.commit()
            print(f"✅ Admin já existia, senha atualizada: {ADMIN_EMAIL}")

        # Criar token JWT
        token = create_access_token({"sub": user.email})
        print(f"\n🔑 Token JWT:\n{token}\n")

        # Decodificar validade
        decoded = jwt.get_unverified_claims(token)
        exp = datetime.utcfromtimestamp(decoded["exp"])
        # Fix DeprecationWarning by using timestamp math if needed, but keeping original logic for now
        days_valid = (exp - datetime.utcnow()).days
        print(f"⏳ Validade do token: {days_valid} dias, expira em {exp} UTC")

if __name__ == "__main__":
    asyncio.run(seed_and_token())
