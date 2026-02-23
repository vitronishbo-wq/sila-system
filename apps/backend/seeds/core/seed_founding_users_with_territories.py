#!/usr/bin/env python3
"""
Seed script para associar os 4 users fundadores aos seus territórios

Padrão RBAC territorial:
- central@sila.gov.ao    → ADMIN_CENTRAL (territory_id=NULL, acesso nacional)
- prov.huambo@sila.gov.ao → ADMIN_PROVINCIAL (Huambo provincial)
- mun.huambo@sila.gov.ao → ADMIN_MUNICIPAL (Huambo municipality)
- comun.huambo@sila.gov.ao → ADMIN_COMMUNAL (Huambo communal - first commune)

Senha universal: Sila_1983
"""

import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment
backend_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(backend_root / ".env")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "sila_system")
DB_USER = os.getenv("DB_USER", "sila_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Configuration
FOUNDING_USERS = [
    {
        "email": "central@sila.gov.ao",
        "role": "ADMIN_CENTRAL",
        "level": "national",
        "territory_query": None,  # NULL territory = national access
    },
    {
        "email": "prov.huambo@sila.gov.ao",
        "role": "ADMIN_PROVINCIAL",
        "level": "provincial",
        "territory_query": "SELECT id FROM territories WHERE name='Huambo' AND type='PROVINCIAL' LIMIT 1",
    },
    {
        "email": "mun.huambo@sila.gov.ao",
        "role": "ADMIN_MUNICIPAL",
        "level": "municipal",
        "territory_query": """
            SELECT id FROM territories 
            WHERE name='Huambo' AND type='MUNICIPAL' 
            AND parent_id = (SELECT id FROM territories WHERE name='Huambo' AND type='PROVINCIAL')
            LIMIT 1
        """,
    },
    {
        "email": "comun.huambo@sila.gov.ao",
        "role": "ADMIN_COMMUNAL",
        "level": "communal",
        "territory_query": """
            SELECT id FROM territories 
            WHERE type='COMMUNAL' 
            AND parent_id IN (
                SELECT id FROM territories 
                WHERE name='Huambo' AND type='MUNICIPAL'
                AND parent_id = (SELECT id FROM territories WHERE name='Huambo' AND type='PROVINCIAL')
            )
            ORDER BY name LIMIT 1
        """,
    },
]


def main():
    """Associate founding users to territories"""
    
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
        print("🔗 ASSOCIANDO USUÁRIOS FUNDADORES A TERRITÓRIOS")
        print("=" * 80)
        
        updated_count = 0
        
        for user_config in FOUNDING_USERS:
            email = user_config["email"]
            role = user_config["role"]
            level = user_config["level"]
            territory_id = None
            
            # Resolve territory if needed
            if user_config["territory_query"]:
                cursor.execute(user_config["territory_query"])
                result = cursor.fetchone()
                if result:
                    territory_id = result[0]
                    cursor.execute(
                        """SELECT name FROM territories WHERE id=%s""",
                        (territory_id,)
                    )
                    terr_name = cursor.fetchone()[0]
                    print(f"\n  📍 {email}")
                    print(f"     Role: {role:20} | Level: {level:12} | Territory: {terr_name}")
                else:
                    print(f"\n  ⚠️  {email} - Território não encontrado!")
                    continue
            else:
                print(f"\n  🌍 {email}")
                print(f"     Role: {role:20} | Level: {level:12} | Territory: NATIONAL (NULL)")
            
            # Update user with territory_id, role, level
            cursor.execute(
                """
                UPDATE users 
                SET region_id = %s, level = %s, status = %s
                WHERE email = %s
                """,
                (territory_id, level, "ACTIVE", email)
            )
            
            if cursor.rowcount > 0:
                updated_count += 1
                print(f"     ✅ Atualizado")
            else:
                print(f"     ⚠️  Usuário não encontrado")
        
        conn.commit()
        
        print("\n" + "=" * 80)
        print("📊 RESULTADO")
        print("=" * 80)
        print(f"  ✅ {updated_count} usuários associados a territórios")
        
        # Validação final
        print("\n" + "=" * 80)
        print("✅ VALIDAÇÃO: Usuários com territórios")
        print("=" * 80)
        cursor.execute("""
            SELECT 
                iu.email,
                iu.role,
                iu.level,
                COALESCE(t.name, 'NACIONAL') as territory_name,
                t.type as territory_type
            FROM iam_users iu
            LEFT JOIN territories t ON iu.territory_id = t.id
            WHERE iu.email LIKE '%@sila.gov.ao' OR iu.email LIKE '%@gmail.com'
            ORDER BY iu.email
        """)
        
        rows = cursor.fetchall()
        for row in rows:
            print(f"  {row[0]:35} | {row[1]:20} | {row[2]:12} | {row[3]:25} | {row[4]}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ SEED COMPLETADO COM SUCESSO")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        raise


if __name__ == "__main__":
    main()
