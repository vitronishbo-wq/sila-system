#!/usr/bin/env python3
"""
Script para criar usuarios IAM completos:
- Admins (global, provincial, municipal, communal)
- Cidadão de teste
Todos com senha universal: Sila_1983
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
    
    # Senha universal
    universal_password = "Sila_1983"
    password_hash = hash_password(universal_password)
    
    users_data = [
        # Admins
        {
            "username": "central@sila.gov.ao",
            "email": "central@sila.gov.ao",
            "full_name": "Administrador Global",
            "role_name": "ADMIN",
            "department": "TI - SILA Central",
            "position": "Administrador Global",
            "is_superuser": True,
            "citizen_id": None,
        },
        {
            "username": "prov.huambo@sila.gov.ao",
            "email": "prov.huambo@sila.gov.ao",
            "full_name": "Gestor Provincial Huambo",
            "role_name": "MANAGER",
            "department": "Governo Provincial - Huambo",
            "position": "Gestor Provincial",
            "is_superuser": False,
            "citizen_id": None,
        },
        {
            "username": "mun.huambo@sila.gov.ao",
            "email": "mun.huambo@sila.gov.ao",
            "full_name": "Gestor Municipal Huambo",
            "role_name": "MANAGER",
            "department": "Prefeitura Municipal - Huambo",
            "position": "Gestor Municipal",
            "is_superuser": False,
            "citizen_id": None,
        },
        {
            "username": "comun.huambo@sila.gov.ao",
            "email": "comun.huambo@sila.gov.ao",
            "full_name": "Funcionário Comunal Huambo",
            "role_name": "OFFICER",
            "department": "Administração Comunal - Huambo",
            "position": "Funcionário de Atendimento",
            "is_superuser": False,
            "citizen_id": None,
        },
        # Cidadão
        {
            "username": "truman@gmail.com",
            "email": "truman@gmail.com",
            "full_name": "Truman Citizen",
            "role_name": "CITIZEN",
            "department": None,
            "position": None,
            "is_superuser": False,
            "citizen_id": str(uuid.uuid4()),
        },
    ]
    
    try:
        print("=" * 60)
        print("🌱 SEED COMPLETO DE USUARIOS IAM + CITIZEN")
        print("=" * 60)
        
        with engine.connect() as conn:
            with conn.begin():
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
                        print(f"⏩ {user_email} já existe - pulando")
                        continue
                    
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
                    
                    # Buscar role
                    role_name = user_data["role_name"]
                    result = conn.execute(
                        text("SELECT id FROM iam_roles WHERE name = :name"),
                        {"name": role_name}
                    )
                    role = result.fetchone()
                    
                    if role:
                        # Vincular role
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
                print("  1. central@sila.gov.ao        → ADMIN (global)")
                print("  2. prov.huambo@sila.gov.ao    → MANAGER (provincial)")
                print("  3. mun.huambo@sila.gov.ao     → MANAGER (municipal)")
                print("  4. comun.huambo@sila.gov.ao   → OFFICER (communal)")
                print("\n👤 CIDADÃO:")
                print("  5. truman@gmail.com           → CITIZEN")
                print("\n🔑 SENHA UNIVERSAL: Sila_1983")
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
