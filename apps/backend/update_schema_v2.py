import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def update():
    url = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    engine = create_async_engine(url)
    
    # Comandos corrigidos (usando aspas simples para valores de texto)
    commands = [
        'ALTER TABLE users ADD COLUMN IF NOT EXISTS uuid UUID DEFAULT gen_random_uuid()',
        'ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20)',
        'ALTER TABLE users ADD COLUMN IF NOT EXISTS bi_number VARCHAR(20)',
        'ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE',
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'ACTIVE'",
        'ALTER TABLE users ADD COLUMN IF NOT EXISTS region_id UUID',
        'ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE',
        'ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP WITH TIME ZONE'
    ]
    for cmd in commands:
        try:
            async with engine.begin() as conn:
                await conn.execute(text(cmd))
            print(f"✅ Sucesso: {cmd[:40]}...")
        except Exception as e:
            print(f"🟡 Ignorado (Já existe ou erro leve): {cmd[:30]}")

    try:
        async with engine.begin() as conn:
            await conn.execute(text("UPDATE users SET uuid = id WHERE uuid IS NULL"))
            print("✨ Sincronização de UUID concluída!")
    except Exception as e:
        print(f"❌ Erro no sincronismo: {e}")
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(update())
