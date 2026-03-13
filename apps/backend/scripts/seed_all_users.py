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
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
import uuid
from datetime import datetime
import bcrypt

from app.core.settings import settings


def hash_password(password: str) -> str:
    """Hash de senha com bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed_all_users():
    """Cria todos os usuários do sistema"""
    
    # Converter DATABASE_URL de asyncpg para postgresql sync
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    # Configurar engine
    engine = create_engine(sync_url, echo=False)
    
    # Senha universal (ambiente de desenvolvimento)
    universal_password = os.getenv("SILA_DEV_UNIVERSAL_PASSWORD", "Sila_1983")
    password_hash = hash_password(universal_password)
    
    users_data = [
        # Admins
        {
            "username": "central@sila.gov.ao",
            "email": "central@sila.gov.ao",
            "full_name": "Administrador Global",
            "role_names": ["SUPERADMIN"],
            "department": "TI - SILA Central",
            "position": "Administrador Global",
            "is_superuser": True,
            "citizen_id": None,
        },
        {
            "username": "admin@sila.gov.ao",
            "email": "admin@sila.gov.ao",
            "full_name": "Administrador de Plataforma",
            "role_names": ["ADMIN", "SUPERADMIN"],
            "department": "TI - SILA Central",
            "position": "Administrador",
            "is_superuser": True,
            "citizen_id": None,
        },
        {
            "username": "prov.huambo@sila.gov.ao",
            "email": "prov.huambo@sila.gov.ao",
            "full_name": "Gestor Provincial Huambo",
            "role_names": ["MANAGER"],
            "department": "Governo Provincial - Huambo",
            "position": "Gestor Provincial",
            "is_superuser": False,
            "citizen_id": None,
        },
        {
            "username": "mun.huambo@sila.gov.ao",
            "email": "mun.huambo@sila.gov.ao",
            "full_name": "Gestor Municipal Huambo",
            "role_names": ["MANAGER"],
            "department": "Prefeitura Municipal - Huambo",
            "position": "Gestor Municipal",
            "is_superuser": False,
            "citizen_id": None,
        },
        {
            "username": "comun.huambo@sila.gov.ao",
            "email": "comun.huambo@sila.gov.ao",
            "full_name": "Gestor Comunal Huambo",
            "role_names": ["MANAGER"],
            "department": "Administração Comunal - Huambo",
            "position": "Gestor Comunal",
            "is_superuser": False,
            "citizen_id": None,
        },
        # Cidadão
        {
            "username": "truman@gmail.com",
            "email": "truman@gmail.com",
            "full_name": "Truman Citizen",
            "role_names": ["CITIZEN"],
            "department": None,
            "position": None,
            "is_superuser": False,
            # Keep nullable unless an existing citizenship citizen UUID is provided.
            "citizen_id": os.getenv("SILA_DEV_TRUMAN_CITIZEN_ID"),
        },
    ]
    
    try:
        print("=" * 60)
        print("🌱 SEED COMPLETO DE USUARIOS IAM + CITIZEN")
        print("=" * 60)
        
        with engine.connect() as conn:
            with conn.begin():
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
                        text("SELECT id FROM iam_users WHERE email = :email"),
                        {"email": user_email}
                    )
                    existing = result.fetchone()
                    
                    if existing:
                        user_id = existing[0]
                        conn.execute(
                            text(
                                """
                                UPDATE iam_users
                                SET username = :username,
                                    password_hash = :password_hash,
                                    citizen_id = :citizen_id,
                                    full_name = :full_name,
                                    department = :department,
                                    position = :position,
                                    status = :status,
                                    is_superuser = :is_superuser,
                                    is_active = :is_active
                                WHERE id = :id
                                """
                            ),
                            {
                                "id": user_id,
                                "username": user_data["username"],
                                "password_hash": password_hash,
                                "citizen_id": user_data["citizen_id"],
                                "full_name": user_data["full_name"],
                                "department": user_data["department"],
                                "position": user_data["position"],
                                "status": "ACTIVE",
                                "is_superuser": user_data["is_superuser"],
                                "is_active": True,
                            },
                        )
                        print(f"♻️  Atualizado: {user_email}")
                    else:
                        # Criar usuário
                        user_id = str(uuid.uuid4())
                        conn.execute(
                            text("""
                                INSERT INTO iam_users (
                                    id, username, email, password_hash, citizen_id,
                                    full_name, department, position, phone, status,
                                    is_superuser, mfa_enabled, mfa_type,
                                    failed_login_attempts, created_at, is_active
                                ) VALUES (
                                    :id, :username, :email, :password_hash, :citizen_id,
                                    :full_name, :department, :position, :phone, :status,
                                    :is_superuser, :mfa_enabled, :mfa_type,
                                    :failed_login_attempts, :created_at, :is_active
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
                                "phone": None,
                                "status": "ACTIVE",
                                "is_superuser": user_data["is_superuser"],
                                "mfa_enabled": False,
                                "mfa_type": "NONE",
                                "failed_login_attempts": 0,
                                "created_at": datetime.utcnow(),
                                "is_active": True,
                            }
                        )
                        print(f"✅ Criado: {user_email}")

                    # Vincular roles
                    for role_name in user_data["role_names"]:
                        role = conn.execute(
                            text("SELECT id FROM iam_roles WHERE name = :name"),
                            {"name": role_name}
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
                            }
                        )
                        print(f"   ├─ Role {role_name} vinculada")
                
                print("\n" + "=" * 60)
                print("📊 RESUMO FINAL")
                print("=" * 60)
                print("\n🔐 CREDENCIAIS DE ACESSO:")
                print("\n👨‍💼 ADMINS:")
                print("  1. central@sila.gov.ao        → SUPERADMIN")
                print("  2. admin@sila.gov.ao          → ADMIN + SUPERADMIN")
                print("  3. prov.huambo@sila.gov.ao    → MANAGER")
                print("  4. mun.huambo@sila.gov.ao     → MANAGER")
                print("  5. comun.huambo@sila.gov.ao   → MANAGER")
                print("\n👤 CIDADÃO:")
                print("  6. truman@gmail.com           → CITIZEN")
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
