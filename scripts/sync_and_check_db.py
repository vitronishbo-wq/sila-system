#!/usr/bin/env python3
"""
Database Alignment and Population Check
Valida alinhamento entre modelo código e banco de dados
Verifica população com: Territórios, Usuário Admin, Cidadão
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add apps/backend to path for imports
sys.path.insert(0, '/home/dev03wsl/sila-system/apps/backend')
os.chdir('/home/dev03wsl/sila-system/apps/backend')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text, inspect
from sqlalchemy.orm import sessionmaker

# Load env
from dotenv import load_dotenv
load_dotenv('/home/dev03wsl/sila-system/.env')

DATABASE_URL = os.getenv('DATABASE_URL')

class DBAlignmentCheck:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False
        )
        self.status = {
            'schema_ok': True,
            'territories': 0,
            'admin_users': 0,
            'citizen_users': 0,
            'citizens': 0,
            'issues': []
        }

    async def check_tables_exist(self):
        """Verifica se as tabelas principais existem"""
        print("\n" + "="*80)
        print("🔍 VERIFICAÇÃO DE SCHEMA - TABELAS PRINCIPAIS")
        print("="*80)
        
        async with self.engine.begin() as conn:
            # Get all table names
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
        
        required_tables = [
            ('users', 'Usuários (legacy)'),
            ('iam_users', 'Usuários (novo sistema IAM)'),
            ('locations', 'Territórios'),
            ('citizenship_citizens', 'Cidadãos (FUC)'),
            ('iam_roles', 'Roles'),
            ('iam_user_roles', 'Atribuição de Roles'),
        ]
        
        print(f"\n📊 Total de tabelas encontradas: {len(tables)}")
        
        for table_name, description in required_tables:
            if table_name in tables:
                print(f"  ✅ {table_name:<30} - {description}")
            else:
                print(f"  ❌ {table_name:<30} - {description}")
                self.status['issues'].append(f"Tabela ausente: {table_name}")
                self.status['schema_ok'] = False
        
        return self.status['schema_ok']



    async def check_population(self):
        """Verifica população de dados"""
        print("\n" + "="*80)
        print("📊 VERIFICAÇÃO DE POPULAÇÃO DE DADOS")
        print("="*80)
        
        async with self.SessionLocal() as session:
            queries = {
                'Usuários (tabela legacy users)': 'SELECT COUNT(*) FROM users',
                'Usuários IAM (iam_users)': 'SELECT COUNT(*) FROM iam_users',
                'Usuários Admin': """
                    SELECT COUNT(*) 
                    FROM users 
                    WHERE roles::text LIKE '%admin%'
                """,
                'Territórios (locations)': 'SELECT COUNT(*) FROM locations',
                'Províncias': "SELECT COUNT(*) FROM locations WHERE type = 'province'",
                'Municípios': "SELECT COUNT(*) FROM locations WHERE type = 'municipality'",
                'Comunas': "SELECT COUNT(*) FROM locations WHERE type = 'commune'",
                'Cidadãos (citizenship_citizens)': 'SELECT COUNT(*) FROM citizenship_citizens',
            }
            
            for label, query in queries.items():
                try:
                    result = await session.execute(text(query))
                    count = result.scalar()
                    
                    if 'Admin' in label:
                        self.status['admin_users'] = count
                    elif 'citizenship_citizens' in label:
                        self.status['citizens'] = count
                        if count == 0:
                            self.status['issues'].append("⚠️ citizenship_citizens vazia")
                    elif 'Territórios' in label:
                        self.status['territories'] = count
                        if count == 0:
                            self.status['issues'].append("⚠️ locations vazia")
                    
                    status = "✅" if count > 0 else "⚠️ VAZIO"
                    print(f"  {label:<45} {status} {count:>6}")
                except Exception as e:
                    print(f"  {label:<45} ❌ ERRO: {str(e)[:30]}")
                    self.status['issues'].append(f"Erro em {label}")

    async def check_admin_user(self):
        """Verifica detalhes do usuário admin"""
        print("\n" + "="*80)
        print("🔐 DETALHES DO USUÁRIO ADMIN (tabela users)")
        print("="*80)
        
        async with self.SessionLocal() as session:
            try:
                result = await session.execute(text("""
                    SELECT 
                        id, email, is_active, roles, created_at
                    FROM users 
                    WHERE roles::text LIKE '%admin%'
                    LIMIT 1
                """))
                admin = result.fetchone()
                
                if admin:
                    print(f"\n✅ Admin encontrado:")
                    print(f"   ID: {admin[0]}")
                    print(f"   Email: {admin[1]}")
                    print(f"   Status: {'Ativo ✅' if admin[2] else 'Inativo ❌'}")
                    print(f"   Roles: {admin[3]}")
                    print(f"   Criado em: {admin[4]}")
                else:
                    print("\n⚠️ Nenhum admin encontrado")
                    self.status['issues'].append("Sem admin no banco de dados")
            except Exception as e:
                print(f"\n❌ Erro ao buscar admin: {e}")

    async def check_citizen_data(self):
        """Verifica dados de exemplo cidadão"""
        print("\n" + "="*80)
        print("👥 AMOSTRA DE CIDADÃO")
        print("="*80)
        
        async with self.SessionLocal() as session:
            try:
                result = await session.execute(text("""
                    SELECT id, name, email, phone, is_active, created_at
                    FROM citizenship_citizens
                    LIMIT 1
                """))
                citizen = result.fetchone()
                
                if citizen:
                    print(f"\n✅ Cidadão encontrado:")
                    print(f"   ID: {citizen[0]}")
                    print(f"   Nome: {citizen[1]}")
                    print(f"   Email: {citizen[2] or '-'}")
                    print(f"   Telefone: {citizen[3] or '-'}")
                    print(f"   Ativo: {citizen[4]}")
                    print(f"   Criado em: {citizen[5]}")
                else:
                    print("\n⚠️ Nenhum cidadão encontrado")
                    self.status['issues'].append("Tabela citizenship_citizens vazia")
            except Exception as e:
                print(f"\n❌ Erro ao buscar cidadão: {e}")

    async def check_territories(self):
        """Verifica territórios"""
        print("\n" + "="*80)
        print("🗺️  AMOSTRA DE TERRITÓRIOS")
        print("="*80)
        
        async with self.SessionLocal() as session:
            try:
                result = await session.execute(text("""
                    SELECT id, name, type, parent_id
                    FROM locations
                    ORDER BY type, id
                    LIMIT 10
                """))
                territories = result.fetchall()
                
                if territories:
                    print(f"\n✅ Territórios encontrados ({len(territories)} amostras):")
                    print(f"\n   {'ID':<6} {'Nome':<30} {'Tipo':<15} {'Parent':<6}")
                    print("   " + "="*65)
                    for terr in territories:
                        parent_str = str(terr[3]) if terr[3] else '-'
                        print(f"   {terr[0]:<6} {str(terr[1])[:30]:<30} {str(terr[2]):<15} {parent_str:<6}")
                else:
                    print("\n⚠️ Nenhum território encontrado")
                    self.status['issues'].append("Tabela locations vazia")
            except Exception as e:
                print(f"\n❌ Erro ao buscar territórios: {e}")

    async def generate_report(self):
        """Gera relatório final"""
        print("\n" + "="*80)
        print("📋 RELATÓRIO FINAL DE ALINHAMENTO")
        print("="*80)
        
        print(f"""
Territórios cadastrados:       {self.status['territories']} {'✅ OK' if self.status['territories'] > 0 else '⚠️ VAZIO'}
Usuários Admin:                {self.status['admin_users']} {'✅ OK' if self.status['admin_users'] > 0 else '⚠️ VAZIO'}
Cidadãos no FUC:               {self.status['citizens']} {'✅ OK' if self.status['citizens'] > 0 else '⚠️ VAZIO'}
""")
        
        if self.status['issues']:
            print("\n⚠️ QUESTÕES IDENTIFICADAS:")
            for i, issue in enumerate(self.status['issues'], 1):
                print(f"   {i}. {issue}")
        
        # Status geral
        print("\n" + "="*80)
        if self.status['territories'] > 0 and self.status['admin_users'] > 0 and self.status['citizens'] > 0:
            print("✅ 🟢 BANCO DE DADOS ALINHADO E POPULADO")
            print("\n   ✅ Territórios: Presentes")
            print("   ✅ Admin: Presente")
            print("   ✅ Cidadão: Presente")
        else:
            print("⚠️ 🟡 SCHEMA OK, MAS DADOS INCOMPLETOS")
            if self.status['territories'] == 0:
                print("\n   ⚠️  Territórios: VAZIO")
            if self.status['admin_users'] == 0:
                print("   ⚠️  Admin: VAZIO")
            if self.status['citizens'] == 0:
                print("   ⚠️  Cidadão: VAZIO")
        print("="*80 + "\n")

    async def run(self):
        """Executa verificação completa"""
        try:
            await self.check_tables_exist()
            await self.check_population()
            await self.check_admin_user()
            await self.check_citizen_data()
            await self.check_territories()
            await self.generate_report()
        finally:
            await self.engine.dispose()


async def main():
    checker = DBAlignmentCheck()
    await checker.run()


if __name__ == "__main__":
    asyncio.run(main())
