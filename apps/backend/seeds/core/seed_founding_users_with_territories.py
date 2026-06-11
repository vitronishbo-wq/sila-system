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

import json
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load environment
backend_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(backend_root / ".env")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "sila_db")
DB_USER = os.getenv("DB_USER", "sila_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Configuration
FOUNDING_USERS = [
    # Apenas o usuário central/super admin é referenciado no fluxo de bootstrap.
    {
        "email": "admin@sila.gov.ao",
        "role": "ADMIN_CENTRAL",
        "level": "national",
        "territory_query": None,  # NULL territory = national access
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
                        """SELECT name FROM locations WHERE id=%s""",
                        (territory_id,),
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

            # Update iam_users with territory metadata
            cursor.execute(
                """
                UPDATE iam_users
                SET custom_metadata = COALESCE(custom_metadata, '{}'::jsonb) || %s::jsonb,
                    status = %s,
                    is_active = true
                WHERE email = %s
                """,
                (
                    json.dumps(
                        {
                            "administrative_level": level.upper(),
                            "territory_id": str(territory_id) if territory_id else None,
                            "territory_name": terr_name if territory_id else "NACIONAL",
                        }
                    ),
                    "ACTIVE",
                    email,
                ),
            )

            if cursor.rowcount > 0:
                updated_count += 1
                print("     ✅ Atualizado")
            else:
                print("     ⚠️  Usuário não encontrado")

        conn.commit()

        print("\n" + "=" * 80)
        print("📊 RESULTADO")
        print("=" * 80)
        print(f"  ✅ {updated_count} usuários associados a territórios")

        # Validação final
        print("\n" + "=" * 80)
        print("✅ VALIDAÇÃO: Usuários com territórios")
        print("=" * 80)
        cursor.execute(
            """
            SELECT
                iu.email,
                COALESCE(array_agg(r.name ORDER BY r.name) FILTER (WHERE r.name IS NOT NULL), ARRAY[]::text[]) as roles,
                iu.custom_metadata->>'administrative_level' as administrative_level,
                COALESCE(l.name, 'NACIONAL') as territory_name,
                l.type as territory_type
            FROM iam_users iu
            LEFT JOIN iam_user_roles ur
                ON ur.user_id = iu.id AND (ur.is_active IS NULL OR ur.is_active = true)
            LEFT JOIN iam_roles r ON r.id = ur.role_id
            LEFT JOIN locations l
                ON l.id = NULLIF(iu.custom_metadata->>'territory_id', '')::uuid
            WHERE iu.email LIKE '%@sila.gov.ao' OR iu.email LIKE '%@gmail.com'
            GROUP BY iu.email, iu.custom_metadata, l.name, l.type
            ORDER BY iu.email
            """
        )

        rows = cursor.fetchall()
        for row in rows:
            roles = ", ".join(row[1]) if isinstance(row[1], list) else str(row[1] or "")
            admin_level = str(row[2] or "")
            territory_name = str(row[3] or "")
            territory_type = str(row[4] or "")
            print(
                f"  {row[0]:35} | {roles:20} | {admin_level:12} | {territory_name:25} | {territory_type}"
            )

        cursor.close()
        conn.close()

        print("\n✅ SEED COMPLETADO COM SUCESSO")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        raise


if __name__ == "__main__":
    main()
