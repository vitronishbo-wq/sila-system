import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def seed():
    url = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    engine = create_async_engine(url)

    provinces = [
        'Bengo', 'Benguela', 'Bié', 'Cabinda', 'Cuando Cubango', 
        'Cuanza Norte', 'Cuanza Sul', 'Cunene', 'Huambo', 'Huíla', 
        'Luanda', 'Lunda Norte', 'Lunda Sul', 'Malanje', 'Moxico', 
        'Namibe', 'Uíge', 'Zaire', 'Icolo e Bengo', 'Moxico Leste', 'Cuando'
    ]

    async with engine.begin() as conn:
        print("🌍 Inserindo 21 Províncias...")
        for name in provinces:
            await conn.execute(text("""
                INSERT INTO locations (name, type)
                VALUES (:name, 'province')
                ON CONFLICT (name) DO NOTHING;
            """), {"name": name})

        print("🏙️ Criando Município do Huambo...")
        # Busca o ID serial (inteiro) do Huambo
        res = await conn.execute(text("SELECT id FROM locations WHERE name = 'Huambo' LIMIT 1"))
        huambo_id = res.scalar()

        if huambo_id:
            await conn.execute(text("""
                INSERT INTO locations (name, type, parent_id)
                VALUES ('Huambo (Município)', 'municipality', :pid)
                ON CONFLICT (name) DO NOTHING;
            """), {"pid": huambo_id})

    print("✅ Seed concluído!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed())
