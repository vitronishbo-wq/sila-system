import asyncio
import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def reset_db():
    from apps.backend.app.core.config import settings
    from apps.backend.app.core.db.base import Base

    print("🔄 Conectando...")
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.begin() as conn:
        print("🧹 Removendo Schema...")
        await conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        print("🏗️ Recriando Schema...")
        await conn.execute(text("CREATE SCHEMA public"))
        print("🔑 Ajustando Permissões...")
        await conn.execute(text("GRANT ALL ON SCHEMA public TO sila_user"))
        print("🛠️ Criando Tabelas...")
        await conn.run_sync(Base.metadata.create_all)
        print("👤 Criando Admin inicial...")
        print("👤 Criando Admin inicial (usando Argon2)...")
        from passlib.context import CryptContext

        # Trocamos bcrypt por argon2 para evitar o bug de versão
        pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        hashed_pw = pwd_context.hash("admin123")

        sql = text("""INSERT INTO "users" (uuid, email, hashed_password, role, is_active, is_verified, status, administrative_level) 
                      VALUES (:uuid, :email, :pw, :role, true, true, :status, :level)""")

        await conn.execute(
            sql,
            {
                "uuid": str(uuid.uuid4()),
                "email": "admin@sila.gov.ao",
                "pw": hashed_pw,
                "role": "admin",
                "status": "active",
                "level": "CENTRAL",
            },
        )
    print("✅ SUCESSO: Banco pronto e Admin criado!")


if __name__ == "__main__":
    asyncio.run(reset_db())
