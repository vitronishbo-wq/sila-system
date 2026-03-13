
from app.core.security import get_password_hash
from modules.identity.models.user import User
import asyncio
from sqlalchemy import select

async def reset_password():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    from config.settings import settings

    # Criar engine manualmente pois SessionLocal pode ser sincrono ou nao configurado corretamente para scripts
    engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        result = await db.execute(select(User).where(User.email == 'admin@sila.gov.ao'))
        user = result.scalar_one_or_none()
        
        if user:
            new_hash = get_password_hash('Admin123!')
            user.hashed_password = new_hash
            await db.commit()
            print(f'✅ Senha do Admin sincronizada com sucesso! Hash: {new_hash[:20]}...')
        else:
            print('❌ Usuário admin@sila.gov.ao não encontrado.')

if __name__ == "__main__":
    asyncio.run(reset_password())
