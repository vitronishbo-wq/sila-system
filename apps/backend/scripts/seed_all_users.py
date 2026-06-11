#!/usr/bin/env python3
"""
Script para criar usuarios IAM completos:
- Admins (global, provincial, municipal, communal)
- Cidadão de teste
Todos com senha universal: Sila_1983

Opcional:
- SILA_DEV_UNIVERSAL_PASSWORD (default: Sila_1983)
- SILA_DEV_TRUMAN_CITIZEN_ID (UUID existente em citizenship_citizens)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import uuid
from datetime import datetime

import bcrypt
from sqlalchemy import create_engine, text

from apps.backend.app.core.settings import settings


def hash_password(password: str) -> str:
    """Hash de senha com bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_all_users():
    """Cria todos os usuários do sistema"""

    # Converter DATABASE_URL de asyncpg para postgresql sync
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

    # Configurar engine
    engine = create_engine(sync_url, echo=False)

    # Senha universal (ambiente de desenvolvimento)
    universal_password = os.getenv("SILA_DEV_UNIVERSAL_PASSWORD", "Sila_1983")
    password_hash = hash_password(universal_password)

    truman_citizen_id = os.getenv(
        "SILA_DEV_TRUMAN_CITIZEN_ID", "11111111-1983-0501-0000-000000000001"
    )
    truman_citizen_exists = False

    # Para conformidade com GOVERNANCE_RULES: apenas o Super Admin é criado por seeds.
    users_data = [
        {
            "username": "admin@sila.gov.ao",
            "email": "admin@sila.gov.ao",
            "full_name": "SUPER_ADMIN_NACIONAL",
            "role_names": ["SUPERADMIN"],
            "department": "TI - SILA Central",
            "position": "Administrador Global",
            "is_superuser": True,
            "citizen_id": None,
            "phone": None,
            "custom_metadata": {},
        },
    ]

    try:
        print("=" * 60)
        print("🌱 SEED COMPLETO DE USUARIOS IAM + CITIZEN")
        print("=" * 60)

        with engine.connect() as conn:
            with conn.begin():
                resolved_citizen_id = truman_citizen_id
                if truman_citizen_id:
                    row = conn.execute(
                        text("SELECT id FROM citizenship_citizens WHERE id = :id LIMIT 1"),
                        {"id": truman_citizen_id},
                    ).fetchone()
                    if row:
                        truman_citizen_exists = True
                    else:
                        row = conn.execute(
                            text(
                                "SELECT id FROM citizenship_citizens WHERE lower(email) = lower(:email) LIMIT 1"
                            ),
                            {"email": "truman@gmail.com"},
                        ).fetchone()
                        if row:
                            resolved_citizen_id = row[0]
                            truman_citizen_exists = True
                        else:
                            residence_row = conn.execute(
                                text(
                                    "SELECT id FROM locations WHERE name = :name AND type = :type LIMIT 1"
                                ),
                                {"name": "Luanda", "type": "PROVINCIA"},
                            ).fetchone()
                            residence_location_id = residence_row[0] if residence_row else None
                            conn.execute(
                                text("""
                                INSERT INTO citizenship_citizens (
                                    id, name, email, phone, address, is_active, bi_number, birth_date, residence_location_id
                                ) VALUES (
                                    :id, :name, :email, :phone, :address, :is_active, :bi_number, :birth_date, :residence_location_id
                                )
                                ON CONFLICT (id) DO NOTHING
                                """),
                                {
                                    "id": truman_citizen_id,
                                    "name": "Truman José Sapalo",
                                    "email": "truman@gmail.com",
                                    "phone": None,
                                    "address": None,
                                    "is_active": True,
                                    "bi_number": "001508576HO034",
                                    "birth_date": "1983-05-01",
                                    "residence_location_id": residence_location_id,
                                },
                            )
                            truman_citizen_exists = True
                for entry in users_data:
                    if entry.get("email") == "truman@gmail.com":
                        entry["citizen_id"] = resolved_citizen_id if truman_citizen_exists else None
                        entry.setdefault("custom_metadata", {})["citizen_id"] = resolved_citizen_id
                        break
                # Garantir roles base para atribuicoes
                required_roles = {"SUPERADMIN", "ADMIN", "MANAGER", "CITIZEN"}
                for role_name in required_roles:
                    role_exists = conn.execute(
                        text("SELECT id FROM iam_roles WHERE name = :name"),
                        {"name": role_name},
                    ).fetchone()
                    if not role_exists:
                        conn.execute(
                            text(
                                """
                                INSERT INTO iam_roles (
                                    id, name, description, role_type, is_system, created_at, is_active
                                ) VALUES (
                                    :id, :name, :description, :role_type, :is_system, :created_at, :is_active
                                )
                                """
                            ),
                            {
                                "id": str(uuid.uuid4()),
                                "name": role_name,
                                "description": f"Role de desenvolvimento: {role_name}",
                                "role_type": "SYSTEM",
                                "is_system": True,
                                "created_at": datetime.utcnow(),
                                "is_active": True,
                            },
                        )

                # Para cada usuário
                for user_data in users_data:
                    user_email = user_data["email"]

                    # Verificar se já existe
                    result = conn.execute(
                        text("SELECT id FROM iam_users WHERE email = :email"), {"email": user_email}
                    )
                    existing = result.fetchone()

                    if existing:
                        user_id = existing[0]
                        custom_metadata_json = json.dumps(user_data["custom_metadata"])
                        custom_metadata_json = json.dumps(user_data["custom_metadata"])
                        conn.execute(
                            text(
                                """
                                UPDATE iam_users
                                SET username = :username,
                                    password_hash = :password_hash,
                                    citizen_id = :citizen_id,
                                    full_name = :full_name,
                                    phone = :phone,
                                    department = :department,
                                    position = :position,
                                    status = :status,
                                    is_superuser = :is_superuser,
                                    is_active = :is_active,
                                    custom_metadata = :custom_metadata
                                WHERE id = :id
                                """
                            ),
                            {
                                "id": user_id,
                                "username": user_data["username"],
                                "password_hash": password_hash,
                                "citizen_id": user_data["citizen_id"],
                                "full_name": user_data["full_name"],
                                "phone": user_data["phone"],
                                "department": user_data["department"],
                                "position": user_data["position"],
                                "status": "ACTIVE",
                                "is_superuser": user_data["is_superuser"],
                                "is_active": True,
                                "custom_metadata": custom_metadata_json,
                            },
                        )
                        print(f"♻️  Atualizado: {user_email}")
                    else:
                        # Criar usuário
                        user_id = str(uuid.uuid4())
                        custom_metadata_json = json.dumps(user_data["custom_metadata"])
                        custom_metadata_json = json.dumps(user_data["custom_metadata"])
                        conn.execute(
                            text("""
                                INSERT INTO iam_users (
                                    id, username, email, password_hash, citizen_id,
                                    full_name, department, position, phone, status,
                                    is_superuser, mfa_enabled, mfa_type,
                                    failed_login_attempts, created_at, is_active,
                                    custom_metadata
                                ) VALUES (
                                    :id, :username, :email, :password_hash, :citizen_id,
                                    :full_name, :department, :position, :phone, :status,
                                    :is_superuser, :mfa_enabled, :mfa_type,
                                    :failed_login_attempts, :created_at, :is_active,
                                    :custom_metadata
                                )
                            """),
                            {
                                "id": user_id,
                                "username": user_data["username"],
                                "email": user_data["email"],
                                "password_hash": password_hash,
                                "citizen_id": user_data["citizen_id"],
                                "full_name": user_data["full_name"],
                                "department": user_data["department"],
                                "position": user_data["position"],
                                "phone": user_data["phone"],
                                "status": "ACTIVE",
                                "is_superuser": user_data["is_superuser"],
                                "mfa_enabled": False,
                                "mfa_type": "NONE",
                                "failed_login_attempts": 0,
                                "created_at": datetime.utcnow(),
                                "is_active": True,
                                "custom_metadata": custom_metadata_json,
                            },
                        )
                        print(f"✅ Criado: {user_email}")

                    # Vincular roles
                    for role_name in user_data["role_names"]:
                        role = conn.execute(
                            text("SELECT id FROM iam_roles WHERE name = :name"), {"name": role_name}
                        ).fetchone()
                        if not role:
                            continue

                        has_link = conn.execute(
                            text(
                                """
                                SELECT id FROM iam_user_roles
                                WHERE user_id = :user_id AND role_id = :role_id
                                """
                            ),
                            {"user_id": user_id, "role_id": role[0]},
                        ).fetchone()
                        if has_link:
                            continue
                        conn.execute(
                            text("""
                                INSERT INTO iam_user_roles (id, user_id, role_id, assigned_at, is_active)
                                VALUES (:id, :user_id, :role_id, :assigned_at, :is_active)
                            """),
                            {
                                "id": str(uuid.uuid4()),
                                "user_id": user_id,
                                "role_id": role[0],
                                "assigned_at": datetime.utcnow(),
                                "is_active": True,
                            },
                        )
                        print(f"   ├─ Role {role_name} vinculada")

                # Apenas Super Admin permanece como seed canonical
                users_table_data = [
                    {
                        "email": "admin@sila.gov.ao",
                        "full_name": "SUPER_ADMIN_NACIONAL",
                        "administrative_level": "SUPER",
                        "region_name": None,
                        "region_type": None,
                        "roles": ["SUPERADMIN"],
                    }
                ]

                def resolve_region_id(region_name, region_type):
                    if not region_name or not region_type:
                        return None
                    row = conn.execute(
                        text(
                            "SELECT id FROM locations WHERE name = :name AND type = :type LIMIT 1"
                        ),
                        {"name": region_name, "type": region_type},
                    ).fetchone()
                    return row[0] if row else None

                for entry in users_table_data:
                    region_id = resolve_region_id(entry["region_name"], entry["region_type"])
                    roles_json = json.dumps(entry["roles"])
                    existing_user = conn.execute(
                        text("SELECT id FROM users WHERE email = :email"),
                        {"email": entry["email"]},
                    ).fetchone()
                    if existing_user:
                        conn.execute(
                            text(
                                """
                                UPDATE users
                                SET hashed_password = :hashed_password,
                                    is_active = true,
                                    is_verified = true,
                                    status = :status,
                                    roles = :roles,
                                    administrative_level = :administrative_level,
                                    region_id = :region_id,
                                    full_name = :full_name,
                                    updated_at = now()
                                WHERE email = :email
                                """
                            ),
                            {
                                "email": entry["email"],
                                "hashed_password": password_hash,
                                "status": "ACTIVE",
                                "roles": roles_json,
                                "administrative_level": entry["administrative_level"],
                                "region_id": region_id,
                                "full_name": entry["full_name"],
                            },
                        )
                    else:
                        conn.execute(
                            text(
                                """
                                INSERT INTO users (
                                    email, hashed_password, is_active, is_verified,
                                    status, roles, administrative_level, region_id,
                                    full_name, created_at, updated_at
                                ) VALUES (
                                    :email, :hashed_password, true, true,
                                    :status, :roles, :administrative_level, :region_id,
                                    :full_name, now(), now()
                                )
                                """
                            ),
                            {
                                "email": entry["email"],
                                "hashed_password": password_hash,
                                "status": "ACTIVE",
                                "roles": roles_json,
                                "administrative_level": entry["administrative_level"],
                                "region_id": region_id,
                                "full_name": entry["full_name"],
                            },
                        )

                # Remover usuário extra (admin@sila.gov.ao) da tabela users
                conn.execute(
                    text("DELETE FROM users WHERE email = :email"),
                    {"email": "admin@sila.gov.ao"},
                )

                print("\n" + "=" * 60)
                print("📊 RESUMO FINAL")
                print("=" * 60)
                print("\n\n🔐 CREDENCIAIS DE ACESSO (SEED):")
                print("\n👨‍💼 ADMINS:")
                print("  1. admin@sila.gov.ao          → SUPERADMIN (bootstrap only)")
                print(f"\n🔑 SENHA UNIVERSAL: {universal_password}")
                print("\n" + "=" * 60)
                print("✅ SEED CONCLUÍDO COM SUCESSO!")
                print("=" * 60)

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        engine.dispose()


if __name__ == "__main__":
    seed_all_users()
