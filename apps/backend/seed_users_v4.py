import asyncio
import bcrypt
import json
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def seed():
    url = "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
    engine = create_async_engine(url)
    
    # Hash da senha Sila_1983
    hashed = bcrypt.hashpw("Sila_1983".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async with engine.begin() as conn:
        print("👤 Buscando IDs de localização...")
        res_prov = await conn.execute(text("SELECT id FROM locations WHERE name = 'Huambo' LIMIT 1"))
        huambo_prov_id = res_prov.scalar()
        
        res_mun = await conn.execute(text("SELECT id FROM locations WHERE name = 'Huambo (Município)' LIMIT 1"))
        huambo_mun_id = res_mun.scalar()

        users = [
            ('central@sila.gov.ao', '["ADMIN"]', 'SUPER ADMIN', 'FEDERAL', None),
            ('prov.huambo@sila.gov.ao', '["MANAGER"]', 'GOV PROVINCIAL HUAMBO', 'PROVINCIAL', huambo_prov_id),
            ('mun.huambo@sila.gov.ao', '["MANAGER"]', 'ADM MUNICIPAL HUAMBO', 'MUNICIPAL', huambo_mun_id),
            ('truman@gmail.com', '["CITIZEN"]', 'TRUMAN MARCELO', 'CITIZEN', None)
        ]

        print("🚀 Inserindo usuários...")
        for email, roles, full_name, level, rid in users:
            # Usamos CAST(:roles AS JSONB) para evitar o erro do "::"
            await conn.execute(text("""
                INSERT INTO users (id, email, hashed_password, full_name, roles, is_active, administrative_level, region_id, status)
                VALUES (gen_random_uuid(), :email, :pw, :name, CAST(:roles AS JSONB), true, :level, :rid, 'ACTIVE')
                ON CONFLICT (email) DO UPDATE SET 
                    region_id = EXCLUDED.region_id,
                    administrative_level = EXCLUDED.administrative_level;
            """), {
                "email": email, 
                "pw": hashed, 
                "name": full_name,
                "roles": roles, # Já passamos como string formatada de JSON
                "level": level, 
                "rid": rid
            })
            
    print("✅ Usuários prontos para teste!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed())
