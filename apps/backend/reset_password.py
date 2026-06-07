import asyncio

from core.security import get_password_hash
from sqlalchemy import select

from apps.backend.app.modules.identity.models.user import User


async def reset_password():
    from config.settings import settings
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

    # Criar engine manualmente pois SessionLocal pode ser sincrono ou nao configurado corretamente para scripts
    engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        result = await db.execute(select(User).where(User.email == "admin@sila.gov.ao"))
        user = result.scalar_one_or_none()

        if user:
            new_hash = get_password_hash("Admin123!")
            user.hashed_password = new_hash
            await db.commit()
            print(f"✅ Senha do Admin sincronizada com sucesso! Hash: {new_hash[:20]}...")
        else:
            print("❌ Usuário admin@sila.gov.ao não encontrado.")


if __name__ == "__main__":
    asyncio.run(reset_password())
