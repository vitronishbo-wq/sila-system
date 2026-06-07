import asyncio
import os
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import select

# Adiciona o root do backend ao path
backend_root = Path(__file__).resolve().parent.parent.parent
# PYTHONPATH should be configured via setup_dev_env.sh; do not mutate sys.path here.

# Carrega variáveis de ambiente do .env
load_dotenv(backend_root / ".env")

from apps.backend.app.core.db import AsyncSessionLocal  # noqa: E402
from config.settings import settings  # noqa: E402
from core.security import get_password_hash  # noqa: E402

from apps.backend.app.modules.identity.models.user import User  # noqa: E402
from apps.backend.core.auth import JWTHandler  # noqa: E402

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
                is_active=True,
            )
            session.add(user)
            await session.commit()
            print(f"✅ Admin criado: {ADMIN_EMAIL}")
        else:
            user.password_hash = get_password_hash(ADMIN_PASSWORD)
            await session.commit()
            print(f"✅ Admin já existia, senha atualizada: {ADMIN_EMAIL}")

        # Criar token JWT
        jwt_handler = JWTHandler(secret_key=settings.SECRET_KEY)
        token = jwt_handler.create_access_token(subject=user.email)
        print(f"\n🔑 Token JWT:\n{token}\n")

        # Decodificar validade
        import jwt

        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = datetime.utcfromtimestamp(decoded["exp"])
        # Fix DeprecationWarning by using timestamp math if needed, but keeping original logic for now
        days_valid = (exp - datetime.utcnow()).days
        print(f"⏳ Validade do token: {days_valid} dias, expira em {exp} UTC")


if __name__ == "__main__":
    asyncio.run(seed_and_token())
