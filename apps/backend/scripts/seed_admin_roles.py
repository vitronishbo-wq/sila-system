#!/usr/bin/env python3
"""
Script para criar roles governamentais e vincular aos admins
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
import uuid
from datetime import datetime

from apps.backend.app.core.settings import settings


def seed_admin_roles():
    """Cria roles ADMIN, MANAGER, OFFICER e vincula aos usuários"""
    
    # Converter DATABASE_URL de asyncpg para postgresql sync
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    # Configurar engine
    engine = create_engine(sync_url, echo=False)
    
    roles_data = [
        {
            "name": "ADMIN",
            "description": "Administrador Global do SILA",
            "role_type": "SYSTEM",
        },
        {
            "name": "MANAGER",
            "description": "Gestor Provincial/Municipal",
            "role_type": "SYSTEM",
        },
        {
            "name": "OFFICER",
            "description": "Funcionário de Atendimento",
            "role_type": "SYSTEM",
        },
    ]
    
    role_assignments = [
        ("central@sila.gov.ao", "ADMIN"),
        ("prov.huambo@sila.gov.ao", "MANAGER"),
        ("mun.huambo@sila.gov.ao", "MANAGER"),
        ("comun.huambo@sila.gov.ao", "OFFICER"),
    ]
    
    try:
        print("=" * 60)
        print("🎯 SEED DE ROLES GOVERNAMENTAIS")
        print("=" * 60)
        
        with engine.connect() as conn:
            with conn.begin():
                # Criar roles
                print("\n🔧 Criando roles...")
                for role_data in roles_data:
                    # Verificar se já existe
                    result = conn.execute(
                        text("SELECT id FROM iam_roles WHERE name = :name"),
                        {"name": role_data["name"]}
                    )
                    existing = result.fetchone()
                    
                    if existing:
                        role_id = existing[0]
                        print(f"  ⏩ Role {role_data['name']} já existe")
                    else:
                        role_id = str(uuid.uuid4())
                        conn.execute(
                            text("""
                                INSERT INTO iam_roles (id, name, description, role_type, is_system, created_at, is_active)
                                VALUES (:id, :name, :description, :role_type, :is_system, :created_at, :is_active)
                            """),
                            {
                                "id": role_id,
                                "name": role_data["name"],
                                "description": role_data["description"],
                                "role_type": role_data["role_type"],
                                "is_system": True,
                                "created_at": datetime.utcnow(),
                                "is_active": True,
                            }
                        )
                        print(f"  ✅ Criada: {role_data['name']}")
                
                # Vincular roles aos usuários
                print("\n🔗 Vinculando roles aos usuários...")
                for email, role_name in role_assignments:
                    # Obter user_id
                    result = conn.execute(
                        text("SELECT id FROM iam_users WHERE email = :email"),
                        {"email": email}
                    )
                    user_result = result.fetchone()
                    
                    if not user_result:
                        print(f"  ⚠️  Usuário {email} não encontrado")
                        continue
                    
                    user_id = user_result[0]
                    
                    # Obter role_id
                    result = conn.execute(
                        text("SELECT id FROM iam_roles WHERE name = :name"),
                        {"name": role_name}
                    )
                    role_result = result.fetchone()
                    
                    if not role_result:
                        print(f"  ⚠️  Role {role_name} não encontrada")
                        continue
                    
                    role_id = role_result[0]
                    
                    # Verificar se já está vinculada
                    result = conn.execute(
                        text("SELECT id FROM iam_user_roles WHERE user_id = :user_id AND role_id = :role_id"),
                        {"user_id": user_id, "role_id": role_id}
                    )
                    existing_link = result.fetchone()
                    
                    if existing_link:
                        print(f"  ⏩ {email} → {role_name} (já vinculada)")
                    else:
                        conn.execute(
                            text("""
                                INSERT INTO iam_user_roles (id, user_id, role_id, assigned_at, is_active)
                                VALUES (:id, :user_id, :role_id, :assigned_at, :is_active)
                            """),
                            {
                                "id": str(uuid.uuid4()),
                                "user_id": user_id,
                                "role_id": role_id,
                                "assigned_at": datetime.utcnow(),
                                "is_active": True,
                            }
                        )
                        print(f"  ✅ {email} → {role_name}")
                
                print("\n" + "=" * 60)
                print("✅ SEED DE ROLES CONCLUÍDO!")
                print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        engine.dispose()


if __name__ == "__main__":
    seed_admin_roles()
