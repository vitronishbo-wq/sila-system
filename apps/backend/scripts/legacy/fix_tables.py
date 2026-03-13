import asyncio
import uuid
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from passlib.context import CryptContext

async def fix():
    url = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    engine = create_async_engine(url)
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
    hashed = pwd_context.hash("Sila_1983")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS "users" (
        id UUID PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        full_name VARCHAR(255),
        is_active BOOLEAN DEFAULT TRUE,
        administrative_level VARCHAR(50),
        roles JSONB DEFAULT '[]'::jsonb,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        async with engine.begin() as conn:
            await conn.execute(text(create_table_sql))
            print("✅ Tabela 'users' pronta!")
            
            check = await conn.execute(text("SELECT id FROM users WHERE email = 'truman@gmail.com'"))
            if not check.fetchone():
                await conn.execute(text("""
                    INSERT INTO users (id, email, hashed_password, full_name, administrative_level)
                    VALUES (:id, :email, :pw, :name, :level)
                """), {"id": uuid.uuid4(), "email": "truman@gmail.com", "pw": hashed, 
                       "name": "Truman Wilson", "level": "CENTRAL"})
                print("👤 Usuário 'truman@gmail.com' criado!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix())
