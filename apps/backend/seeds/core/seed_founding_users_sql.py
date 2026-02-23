"""
Seed script para os 4 users fundadores de SILA - VERSÃO COM SQL DIRETO (2026-02-22)

Padrão RBAC territorial:
- central@sila.gov.ao      → ADMIN_CENTRAL (acesso nacional, region_id=NULL)
- prov.huambo@sila.gov.ao  → ADMIN_PROVINCIAL (Huambo)
- mun.huambo@sila.gov.ao   → ADMIN_MUNICIPAL (Huambo città)
- comun.huambo@sila.gov.ao → ADMIN_COMMUNAL (communes)

Senha universal: Test1234

Usa SQL direto para evitar problemas de bcrypt
"""

import psycopg2
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env
backend_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(backend_root / ".env")

# Database connection
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "sila_db")
DB_USER = os.getenv("DB_USER", "sila_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Trumanmarcelo_1983")

# ==================== USERS CONFIG ====================
FOUNDING_USERS = [
    {
        "email": "central@sila.gov.ao",
        "full_name": "Administrador Central",
        "administrative_level": "CENTRAL",
        "roles": '["ADMIN", "ADMIN_CENTRAL"]',  # JSON string
        "region_id": None,
    },
    {
        "email": "prov.huambo@sila.gov.ao",
        "full_name": "Administrador Provincial - Huambo",
        "administrative_level": "PROVINCIAL",
        "roles": '["ADMIN", "ADMIN_PROVINCIAL"]',
        "region_id": None,
    },
    {
        "email": "mun.huambo@sila.gov.ao",
        "full_name": "Administrador Municipal - Huambo",
        "administrative_level": "MUNICIPAL",
        "roles": '["ADMIN", "ADMIN_MUNICIPAL"]',
        "region_id": None,
    },
    {
        "email": "comun.huambo@sila.gov.ao",
        "full_name": "Administrador Comunal - Huambo",
        "administrative_level": "COMMUNAL",
        "roles": '["ADMIN", "ADMIN_COMMUNAL"]',
        "region_id": None,
    },
    {
        "email": "truman@gmail.com",
        "full_name": "Cidadão Truman",
        "administrative_level": "LOCAL",
        "roles": '["USER", "CITIZEN"]',
        "region_id": None,
    },
]

def seed_users():
    """Seed dos users usando SQL direto"""
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()
        
        print("=" * 80)
        print("🌱 SEED: Criando users fundadores com SQL")
        print("=" * 80)
        print(f"   Senha universal: Sila_1983")
        print("=" * 80)
        print("")
        
        created_count = 0
        
        # Hash bcrypt pré-calculado para "Sila_1983"
        # Nota: Gerado com: password_hash("Sila_1983")
        PASSWORD_HASH = "$2b$12$Kq7oVMGZOXcqWvL3nY4cXuI7ZQ9.KvYXhVW7rR2nXKzV0Uq0mLHgi"
        
        # DELETE: Remover users existentes para recriar com nova senha
        print("\n🗑️  Limpando users antigos...\n")
        for user_config in FOUNDING_USERS:
            cursor.execute("DELETE FROM users WHERE email = %s", (user_config["email"],))
        conn.commit()
        print("✅ Users antigos removidos com sucesso\n")
        
        for user_config in FOUNDING_USERS:
            email = user_config["email"]
            full_name = user_config["full_name"]
            administrative_level = user_config["administrative_level"]
            roles = user_config["roles"]
            region_id = user_config.get("region_id")
            
            # Inserir novo user com hash bcrypt para senha Sila_1983
            cursor.execute("""
                INSERT INTO users (
                    uuid,
                    email,
                    hashed_password,
                    full_name,
                    phone,
                    bi_number,
                    is_active,
                    is_verified,
                    status,
                    administrative_level,
                    region_id,
                    roles
                ) VALUES (
                    gen_random_uuid(),
                    %s,
                    %s,
                    %s,
                    NULL,
                    NULL,
                    true,
                    true,
                    'ACTIVE',
                    %s,
                    %s,
                    %s::jsonb
                )
            """, (
                email,
                PASSWORD_HASH,  # Hash bcrypt para Sila_1983
                full_name,
                administrative_level,
                region_id,
                roles,
            ))
            
            created_count += 1
            print(f"✅ CRIADO: {email}")
            print(f"   Level: {administrative_level}")
            print(f"   Roles: {roles}")
            
            created_count += 1
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 80)
        print(f"📊 RESULTADO:")
        print(f"   ✅ Criados: {created_count}")
        print("=" * 80)
        
        # Validação final - consultar BD
        print("\n" + "=" * 80)
        print("✅ VALIDAÇÃO: Users cadastrados")
        print("=" * 80)
        
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT email, administrative_level, roles, is_active
            FROM users
            ORDER BY email
        """)
        
        for row in cursor.fetchall():
            email, admin_level, roles_json, is_active = row
            status = "✅ ATIVO" if is_active else "❌ INATIVO"
            print(f"  {email:30} | {admin_level:12} | {roles_json} | {status}")
        
        cursor.close()
        conn.close()
        
        print("=" * 80)
        print("✅ SEED CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)


if __name__ == "__main__":
    seed_users()
