#!/usr/bin/env python3
"""
IAM System Synchronization Script
Sincroniza dados do sistema legacy para o novo IAM

Operações:
1. Cria roles básicas no novo sistema
2. Cria permissões padrão
3. Mapeia usuários legacy → novo IAM (opcional)
4. Popula relacionamentos de roles/permissions
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from uuid import uuid4

sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')
os.chdir('/home/dev03wsl/sila-system/apps/backend')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv('/home/dev03wsl/sila-system/.env')

DATABASE_URL = os.getenv('DATABASE_URL')

# System roles to create
SYSTEM_ROLES = [
    {
        'name': 'SUPERADMIN',
        'description': 'Sistema Super Administrador - Acesso total',
        'role_type': 'SYSTEM',
        'is_system': True,
    },
    {
        'name': 'ADMIN',
        'description': 'Administrador de Sistema',
        'role_type': 'SYSTEM',
        'is_system': True,
    },
    {
        'name': 'MANAGER',
        'description': 'Gestor de Serviços',
        'role_type': 'SYSTEM',
        'is_system': True,
    },
    {
        'name': 'CITIZEN',
        'description': 'Cidadão Comum',
        'role_type': 'SYSTEM',
        'is_system': True,
    },
    {
        'name': 'GUEST',
        'description': 'Visitante do Sistema',
        'role_type': 'SYSTEM',
        'is_system': True,
    },
]

# System permissions
SYSTEM_PERMISSIONS = [
    # Admin permissions
    {'name': 'admin.users.create', 'resource': 'users', 'action': 'create'},
    {'name': 'admin.users.read', 'resource': 'users', 'action': 'read'},
    {'name': 'admin.users.update', 'resource': 'users', 'action': 'update'},
    {'name': 'admin.users.delete', 'resource': 'users', 'action': 'delete'},
    
    # Roles permissions
    {'name': 'admin.roles.create', 'resource': 'roles', 'action': 'create'},
    {'name': 'admin.roles.read', 'resource': 'roles', 'action': 'read'},
    {'name': 'admin.roles.update', 'resource': 'roles', 'action': 'update'},
    {'name': 'admin.roles.delete', 'resource': 'roles', 'action': 'delete'},
    
    # Citizens permissions
    {'name': 'citizen.profile.read', 'resource': 'profile', 'action': 'read'},
    {'name': 'citizen.profile.update', 'resource': 'profile', 'action': 'update'},
    
    # Public permissions
    {'name': 'public.login', 'resource': 'auth', 'action': 'login'},
    {'name': 'public.register', 'resource': 'auth', 'action': 'register'},
]

# Role-Permission mappings
ROLE_PERMISSIONS = {
    'SUPERADMIN': [
        'admin.users.create', 'admin.users.read', 'admin.users.update', 'admin.users.delete',
        'admin.roles.create', 'admin.roles.read', 'admin.roles.update', 'admin.roles.delete',
        'citizen.profile.read', 'citizen.profile.update',
        'public.login', 'public.register',
    ],
    'ADMIN': [
        'admin.users.create', 'admin.users.read', 'admin.users.update', 'admin.users.delete',
        'citizen.profile.read', 'citizen.profile.update',
        'public.login',
    ],
    'MANAGER': [
        'admin.users.read', 'admin.users.update',
        'citizen.profile.read', 'citizen.profile.update',
        'public.login',
    ],
    'CITIZEN': [
        'citizen.profile.read', 'citizen.profile.update',
        'public.login',
    ],
    'GUEST': [
        'public.login', 'public.register',
    ],
}


class IAMSynchronizer:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False
        )

    async def create_role(self, session, role_data):
        """Create a role in the new IAM system"""
        role_id = str(uuid4())
        
        query = text("""
            INSERT INTO iam_roles (id, name, description, role_type, is_system, created_at)
            VALUES (:id, :name, :description, :role_type, :is_system, :created_at)
            ON CONFLICT (name) DO UPDATE SET
                description = EXCLUDED.description,
                updated_at = now()
            RETURNING id, name
        """)
        
        result = await session.execute(query, {
            'id': role_id,
            'name': role_data['name'],
            'description': role_data.get('description'),
            'role_type': role_data.get('role_type', 'CUSTOM'),
            'is_system': role_data.get('is_system', False),
            'created_at': datetime.utcnow(),
        })
        
        return result.fetchone()

    async def create_permission(self, session, perm_data):
        """Create a permission in the new IAM system"""
        perm_id = str(uuid4())
        
        query = text("""
            INSERT INTO iam_permissions (id, name, resource, action, is_system, created_at)
            VALUES (:id, :name, :resource, :action, :is_system, :created_at)
            ON CONFLICT (name) DO UPDATE SET
                resource = EXCLUDED.resource,
                action = EXCLUDED.action,
                updated_at = now()
            RETURNING id, name
        """)
        
        result = await session.execute(query, {
            'id': perm_id,
            'name': perm_data['name'],
            'resource': perm_data['resource'],
            'action': perm_data['action'],
            'is_system': True,
            'created_at': datetime.utcnow(),
        })
        
        return result.fetchone()

    async def link_permission_to_role(self, session, role_name, perm_name):
        """Link a permission to a role"""
        link_id = str(uuid4())
        
        query = text("""
            INSERT INTO iam_role_permissions (id, role_id, permission_id, created_at)
            SELECT :id, r.id, p.id, :created_at
            FROM iam_roles r, iam_permissions p
            WHERE r.name = :role_name AND p.name = :perm_name
            ON CONFLICT (role_id, permission_id) DO NOTHING
            RETURNING id
        """)
        
        await session.execute(query, {
            'id': link_id,
            'role_name': role_name,
            'perm_name': perm_name,
            'created_at': datetime.utcnow(),
        })

    async def sync_roles_and_permissions(self):
        """Sincroniza roles e permissões do sistema"""
        print("\n" + "="*80)
        print("🔄 SINCRONIZAÇÃO DO SISTEMA IAM")
        print("="*80)
        
        async with self.SessionLocal() as session:
            try:
                # 1. Criar roles
                print("\n📋 Criando Roles...")
                role_mapping = {}
                
                for role_data in SYSTEM_ROLES:
                    result = await self.create_role(session, role_data)
                    if result:
                        print(f"   ✅ Role criada/atualizada: {result[1]}")
                        role_mapping[role_data['name']] = result[0]
                
                await session.commit()
                
                # 2. Criar permissions
                print("\n🔐 Criando Permissões...")
                perm_mapping = {}
                
                for perm_data in SYSTEM_PERMISSIONS:
                    result = await self.create_permission(session, perm_data)
                    if result:
                        print(f"   ✅ Permissão criada/atualizada: {result[1]}")
                        perm_mapping[perm_data['name']] = result[0]
                
                await session.commit()
                
                # 3. Vincular permissões às roles
                print("\n🔗 Vinculando Permissões a Roles...")
                
                for role_name, perms in ROLE_PERMISSIONS.items():
                    for perm_name in perms:
                        await self.link_permission_to_role(session, role_name, perm_name)
                    print(f"   ✅ {role_name}: {len(perms)} permissões vinculadas")
                
                await session.commit()
                print("\n✅ Sincronização de Roles e Permissões Completa!")
                
            except Exception as e:
                await session.rollback()
                print(f"\n❌ Erro durante sincronização: {e}")
                raise

    async def verify_iam_tables(self):
        """Verifica se as tabelas IAM foram criadas"""
        print("\n" + "="*80)
        print("🔍 VERIFICAÇÃO DE TABELAS IAM")
        print("="*80)
        
        async with self.SessionLocal() as session:
            tables_to_check = [
                'iam_users',
                'iam_roles',
                'iam_permissions',
                'iam_user_roles',
                'iam_role_permissions',
                'iam_user_permissions',
            ]
            
            query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            
            result = await session.execute(query)
            existing_tables = [row[0] for row in result.fetchall()]
            
            print()
            for table in tables_to_check:
                if table in existing_tables:
                    print(f"   ✅ {table}")
                else:
                    print(f"   ❌ {table}")

    async def show_iam_status(self):
        """Mostra status do sistema IAM"""
        print("\n" + "="*80)
        print("📊 STATUS DO SISTEMA IAM")
        print("="*80)
        
        async with self.SessionLocal() as session:
            queries = {
                'Roles criadas': 'SELECT COUNT(*) FROM iam_roles',
                'Permissões criadas': 'SELECT COUNT(*) FROM iam_permissions',
                'Vinculações role→permission': 'SELECT COUNT(*) FROM iam_role_permissions',
                'Usuários IAM': 'SELECT COUNT(*) FROM iam_users',
                'Vinculações user→role': 'SELECT COUNT(*) FROM iam_user_roles',
            }
            
            print()
            for label, query in queries.items():
                try:
                    result = await session.execute(text(query))
                    count = result.scalar()
                    print(f"   {label:<35} {count:>6}")
                except Exception as e:
                    print(f"   {label:<35} ❌ ERRO")

    async def run(self):
        """Executa sincronização completa"""
        try:
            await self.verify_iam_tables()
            await self.sync_roles_and_permissions()
            await self.show_iam_status()
            print("\n✅ Sincronização IAM finalizada com sucesso!\n")
        finally:
            await self.engine.dispose()


async def main():
    sync = IAMSynchronizer()
    await sync.run()


if __name__ == "__main__":
    asyncio.run(main())
