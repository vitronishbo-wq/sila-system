import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def refactor():
    url = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    engine = create_async_engine(url)

    provinces = [
        'Bengo', 'Benguela', 'Bié', 'Cabinda', 'Cuando Cubango', 
        'Cuanza Norte', 'Cuanza Sul', 'Cunene', 'Huambo', 'Huíla', 
        'Luanda', 'Lunda Norte', 'Lunda Sul', 'Malanje', 'Moxico', 
        'Namibe', 'Uíge', 'Zaire', 'Icolo e Bengo', 'Moxico Leste', 'Cuando'
    ]

    async with engine.begin() as conn:
        print("🧹 Limpando dados antigos para evitar duplicatas...")
        # Desativa chaves estrangeiras temporariamente para limpar
        await conn.execute(text("TRUNCATE TABLE locations CASCADE;"))
        # Reinicia a contagem do ID serial
        await conn.execute(text("ALTER SEQUENCE locations_id_seq RESTART WITH 1;"))

        print("🌍 Inserindo as 21 Províncias oficiais...")
        for name in provinces:
            await conn.execute(text("""
                INSERT INTO locations (name, type)
                VALUES (:name, 'province');
            """), {"name": name})

        print("🏙️ Vinculando Município do Huambo...")
        res = await conn.execute(text("SELECT id FROM locations WHERE name = 'Huambo' LIMIT 1"))
        huambo_id = res.scalar()

        if huambo_id:
            await conn.execute(text("""
                INSERT INTO locations (name, type, parent_id)
                VALUES ('Huambo (Município)', 'municipality', :pid);
            """), {"pid": huambo_id})

    print("✅ Refatoração concluída! 21 Províncias prontas.")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(refactor())
