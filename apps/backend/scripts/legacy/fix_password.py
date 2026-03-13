import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from passlib.context import CryptContext

async def fix():
    # Usando estritamente BCRYPT como o seu log de erro indicou
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    new_hash = pwd_context.hash("Sila_1983")
    
    url = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    engine = create_async_engine(url)
    
    try:
        async with engine.begin() as conn:
            await conn.execute(
                text("UPDATE users SET hashed_password = :pw WHERE email = 'truman@gmail.com'"),
                {"pw": new_hash}
            )
            print("✅ Senha de 'truman@gmail.com' atualizada para formato BCRYPT!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(fix())
