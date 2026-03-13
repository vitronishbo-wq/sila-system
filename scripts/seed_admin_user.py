#!/usr/bin/env python3
"""
Seed Admin User and Verify Population
Popula o banco com usuário admin e valida estado
"""

import asyncio
import os
import sys
from datetime import datetime
import json

sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')
os.chdir('/home/dev03wsl/sila-system/apps/backend')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text, select
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv('/home/dev03wsl/sila-system/.env')

# Try to import User model
try:
    from apps.backend.app.modules.identity.infrastructure.models.user_model import UserModel
    print("✅ Importado UserModel (identity)")
    USE_NEW_MODEL = True
except ImportError:
    print("⚠️  Modelo User novo não encontrado, usando legacy")
    USE_NEW_MODEL = False

from app.core.security import get_password_hash

DATABASE_URL = os.getenv('DATABASE_URL')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@sila.gov.ao')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

print(f"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    SEED DATABASE - ADMIN USER                              ║
╚════════════════════════════════════════════════════════════════════════════╝

Configuração:
  Email: {ADMIN_EMAIL}
  Database: postgresql://{DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}
""")

async def seed_admin():
    """Popula admin na tabela users"""
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False
    )
    
    async with SessionLocal() as session:
        try:
            # Verificar se admin já existe
            print("\n🔍 Verificando se admin já existe...")
            result = await session.execute(
                text("SELECT id, email FROM users WHERE email = :email"),
                {"email": ADMIN_EMAIL}
            )
            existing_admin = result.fetchone()
            
            if existing_admin:
                print(f"✅ Admin já existe: {existing_admin[1]} (ID: {existing_admin[0]})")
                return
            
            # Criar admin
            print(f"\n➕ Criando admin user: {ADMIN_EMAIL}")
            
            roles = ["admin", "superadmin"]
            password_hash = get_password_hash(ADMIN_PASSWORD)
            
            query = text("""
                INSERT INTO users (
                    uuid, email, hashed_password, roles, 
                    is_active, is_verified, status, administrative_level,
                    full_name, created_at, updated_at
                ) VALUES (
                    gen_random_uuid(), :email, :password_hash, :roles,
                    true, true, 'active', 'national',
                    'Admin SILA', now(), now()
                )
                RETURNING id, email, roles
            """)
            
            result = await session.execute(query, {
                "email": ADMIN_EMAIL,
                "password_hash": password_hash,
                "roles": json.dumps(roles)
            })
            
            new_admin = result.fetchone()
            await session.commit()
            
            print(f"✅ Admin criado com sucesso!")
            print(f"   ID: {new_admin[0]}")
            print(f"   Email: {new_admin[1]}")
            print(f"   Roles: {new_admin[2]}")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Erro ao criar admin: {e}")
            raise
        finally:
            await engine.dispose()

async def verify_population():
    """Verifica população final do banco"""
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False
    )
    
    print("\n" + "="*80)
    print("📊 VERIFICAÇÃO FINAL DE POPULAÇÃO")
    print("="*80)
    
    async with SessionLocal() as session:
        queries = {
            '👥 Usuários (users)': 'SELECT COUNT(*) FROM users',
            '🔐 Admins': "SELECT COUNT(*) FROM users WHERE roles::text LIKE '%admin%'",
            '🗺️  Territórios': 'SELECT COUNT(*) FROM locations',
            '🌍 Províncias': "SELECT COUNT(*) FROM locations WHERE type = 'province'",
            '👨 Cidadãos': 'SELECT COUNT(*) FROM citizenship_citizens',
        }
        
        for label, query in queries.items():
            try:
                result = await session.execute(text(query))
                count = result.scalar()
                status = "✅" if count > 0 else "⚠️"
                print(f"  {label:<40} {status} {count:>6}")
            except Exception as e:
                print(f"  {label:<40} ❌ ERRO: {str(e)[:30]}")
    
    await engine.dispose()

async def get_admin_credentials():
    """Retorna credenciais do admin criado"""
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False
    )
    
    async with SessionLocal() as session:
        result = await session.execute(
            text("SELECT id, email, roles FROM users WHERE roles::text LIKE '%admin%' LIMIT 1")
        )
        admin = result.fetchone()
        if admin:
            print("\n" + "="*80)
            print("🔐 CREDENCIAIS DO ADMIN")
            print("="*80)
            print(f"""
Email: {admin[1]}
Senha: {ADMIN_PASSWORD}
Roles: {admin[2]}

Para testar a API:
  curl -X POST http://localhost:8000/api/v1/auth/login \\
    -H "Content-Type: application/json" \\
    -d '{{"email": "{admin[1]}", "password": "{ADMIN_PASSWORD}"}}'
""")
    
    await engine.dispose()

async def main():
    try:
        await seed_admin()
        await verify_population()
        await get_admin_credentials()
        print("\n✅ Seeding concluído com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
