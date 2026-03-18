#!/usr/bin/env python3
"""
Script para criar roles e permissões específicas para cidadãos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
import uuid
from datetime import datetime

from apps.backend.app.core.settings import settings


def seed_citizen_roles():
    """Cria roles e permissões para cidadãos"""
    
    # Converter DATABASE_URL de asyncpg para postgresql sync
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    
    # Configurar engine
    engine = create_engine(sync_url, echo=False)
    
    try:
        print("🌱 Criando role CITIZEN...")
        
        with engine.connect() as conn:
            with conn.begin():
                # Verificar se já existe
                result = conn.execute(
                    text("SELECT id FROM iam_roles WHERE name = :name"),
                    {"name": "CITIZEN"}
                )
                existing = result.fetchone()
                
                if existing:
                    print("✅ Role CITIZEN já existe")
                    citizen_role_id = existing[0]
                else:
                    # Criar role
                    citizen_role_id = str(uuid.uuid4())
                    conn.execute(
                        text("""
                            INSERT INTO iam_roles (id, name, description, role_type, is_system, created_at, is_active)
                            VALUES (:id, :name, :description, :role_type, :is_system, :created_at, :is_active)
                        """),
                        {
                            "id": citizen_role_id,
                            "name": "CITIZEN",
                            "description": "Cidadão comum com acesso a serviços públicos",
                            "role_type": "CUSTOM",
                            "is_system": False,
                            "created_at": datetime.utcnow(),
                            "is_active": True,
                        }
                    )
                    print("✅ Role CITIZEN criada")
                
                print("🔧 Criando permissões para cidadãos...")
                
                # Lista de permissões para cidadãos
                citizen_permissions = [
                    ("citizen:read:self", "citizen", "read:self", "Ler próprio perfil"),
                    ("citizen:update:self", "citizen", "update:self", "Atualizar próprio perfil"),
                    ("dashboard:read:self", "dashboard", "read:self", "Ver dashboard pessoal"),
                    ("notifications:read:self", "notifications", "read:self", "Ver notificações"),
                ]
                
                permission_ids = []
                
                for code, module, action, description in citizen_permissions:
                    # Verificar se permissão já existe
                    result = conn.execute(
                        text("SELECT id FROM iam_permissions WHERE code = :code"),
                        {"code": code}
                    )
                    existing_perm = result.fetchone()
                    
                    if existing_perm:
                        print(f"  ⏩ Permissão já existe: {code}")
                        permission_ids.append(existing_perm[0])
                    else:
                        # Criar permissão
                        perm_id = str(uuid.uuid4())
                        conn.execute(
                            text("""
                                INSERT INTO iam_permissions (id, code, module, resource, action, scope, description, is_system, created_at, is_active)
                                VALUES (:id, :code, :module, :resource, :action, :scope, :description, :is_system, :created_at, :is_active)
                            """),
                            {
                                "id": perm_id,
                                "code": code,
                                "module": module,
                                "resource": module,
                                "action": action,
                                "scope": "OWN" if "self" in action else "NATIONAL",
                                "description": description,
                                "is_system": False,
                                "created_at": datetime.utcnow(),
                                "is_active": True,
                            }
                        )
                        print(f"  ✅ Criada: {code}")
                        permission_ids.append(perm_id)
                
                print("🔗 Vinculando permissões à role CITIZEN...")
                
                # Limpar vínculos existentes
                conn.execute(
                    text("DELETE FROM iam_role_permissions WHERE role_id = :role_id"),
                    {"role_id": citizen_role_id}
                )
                
                # Criar novos vínculos
                for perm_id in permission_ids:
                    conn.execute(
                        text("""
                            INSERT INTO iam_role_permissions (id, role_id, permission_id, created_at, is_active)
                            VALUES (:id, :role_id, :permission_id, :created_at, :is_active)
                        """),
                        {
                            "id": str(uuid.uuid4()),
                            "role_id": citizen_role_id,
                            "permission_id": perm_id,
                            "created_at": datetime.utcnow(),
                            "is_active": True,
                        }
                    )
                
                print(f"✅ {len(permission_ids)} permissões vinculadas à role CITIZEN")
                
                print("\n📊 Resumo:")
                print(f"  Role: CITIZEN")
                print(f"  Permissões: {len(permission_ids)}")
                print("\n🎉 Seeds de cidadão concluídos!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        engine.dispose()


if __name__ == "__main__":
    print("=" * 50)
    print("🌱 SEED DE ROLES E PERMISSÕES PARA CIDADÃOS")
    print("=" * 50)
    seed_citizen_roles()

