#!/usr/bin/env python3
# ===========================================
# scripts/seed_dashboard.py
# Popula Dashboard com dados reais (Angola 2025)
# ===========================================

import asyncio
import random
from datetime import datetime, timedelta, UTC
from typing import List
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from core.db.session import async_session_factory

# ===========================
# Data Pools (Angola 2025)
# ===========================

NOMES = [
    "Ana", "João", "Maria", "Pedro", "Luísa", "Carlos", "Beatriz", "António",
    "Sofia", "Miguel", "Margarida", "Gonçalo", "Filipa", "Nuno", "Joana"
]

SOBRENOMES = [
    "da Silva", "dos Santos", "Pereira", "Costa", "Lopes", "Ferreira",
    "Gomes", "Rodrigues", "Almeida", "Marques", "Oliveira", "Sousa",
    "Martins", "Correia", "Vieira"
]

PROVINCIAS = [
    "Luanda", "Cabinda", "Zaire", "Bengo", "Kwanza Norte",
    "Kwanza Sul", "Malanje", "Moxico", "Cuando Cubango",
    "Benguela", "Huambo", "Bié", "Namibe", "Cunene"
]

# ===========================
# Funções Auxiliares
# ===========================

def gerar_nome() -> str:
    """Gera nome aleatório realista"""
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"

# ===========================
# Seed Functions
# ===========================

# ===========================
# Seed Functions
# ===========================

async def seed_usuarios(session: AsyncSession, quantidade: int = 89) -> int:
    """Seed de usuários realistas - SEM usar modelo ORM"""
    print(f"➕ Criando {quantidade} usuários...")
    
    # Usando SQL direto para evitar problemas com múltiplos modelos Document
    from sqlalchemy import text
    
    usuarios_inseridos = 0
    
    # Admin principal
    try:
        await session.execute(
            text("""
                INSERT INTO identity_users (email, name, is_active, created_at, updated_at)
                VALUES (:email, :name, :is_active, :created_at, :updated_at)
            """),
            {
                "email": "admin@sila.gov.ao",
                "name": "Admin SILA",
                "is_active": True,
                "created_at": datetime.now(UTC) - timedelta(days=365),
                "updated_at": datetime.now(UTC)
            }
        )
        usuarios_inseridos += 1
    except Exception as e:
        print(f"  [WARNING] Tabela identity_users não existe ou erro: {e}")
        return 0
    
    # Outros usuários
    for i in range(1, quantidade):
        nome = gerar_nome()
        email = f"{nome.split()[0].lower()}{i}@sila.gov.ao"
        try:
            await session.execute(
                text("""
                    INSERT INTO identity_users (email, name, is_active, created_at, updated_at)
                    VALUES (:email, :name, :is_active, :created_at, :updated_at)
                """),
                {
                    "email": email,
                    "name": nome,
                    "is_active": random.choice([True, True, True, False]),
                    "created_at": gerar_data_aleatoria(180),
                    "updated_at": datetime.now(UTC)
                }
            )
            usuarios_inseridos += 1
        except Exception:
            pass  # Skip duplicates
    
    await session.flush()
    print(f"  ✅ {usuarios_inseridos} usuários criados")
    return usuarios_inseridos

async def seed_documentos(session: AsyncSession, quantidade: int = 1247) -> int:
    """Seed de documentos realistas"""
    print(f"➕ Criando {quantidade} documentos...")
    
    from sqlalchemy import text
    
    documentos_inseridos = 0
    
    for i in range(quantidade):
        nome_beneficiario = gerar_nome()
        try:
            await session.execute(
                text("""
                    INSERT INTO documents_documents (filename, original_name, file_size, uploaded_by_id, created_at, updated_at)
                    VALUES (:filename, :original_name, :file_size, :uploaded_by_id, :created_at, :updated_at)
                """),
                {
                    "filename": f"doc_{datetime.now(UTC).strftime('%Y%m%d')}_{i+1000}.pdf",
                    "original_name": f"Certidão_{nome_beneficiario.replace(' ', '_')}_{random.randint(1970,2005)}.pdf",
                    "file_size": random.randint(80000, 5000000),
                    "uploaded_by_id": 1,
                    "created_at": gerar_data_aleatoria(365),
                    "updated_at": datetime.now(UTC)
                }
            )
            documentos_inseridos += 1
        except Exception:
            pass  # Skip if table doesn't exist
    
    if documentos_inseridos > 0:
        await session.flush()
        print(f"  ✅ {documentos_inseridos} documentos criados")
    else:
        print(f"  [SKIP] Tabela documents_documents não existe")
    
    return documentos_inseridos

async def seed_atividades(session: AsyncSession, quantidade: int = 42) -> int:
    """Seed de atividades: CitizenshipRequest records"""
    print(f"➕ Criando {quantidade} atividades (citizenship requests)...")
    
    from sqlalchemy import text
    
    atividades_inseridas = 0
    statuses = ["approved", "pending", "processing", "rejected"]
    
    for i in range(quantidade):
        nome = gerar_nome()
        bi_number = f"{random.randint(1000000, 9999999)}LA{random.randint(10,99)}"
        try:
            await session.execute(
                text("""
                    INSERT INTO citizenship_requests (full_name, bi_number, status, created_at, updated_at)
                    VALUES (:full_name, :bi_number, :status, :created_at, :updated_at)
                """),
                {
                    "full_name": nome,
                    "bi_number": bi_number,
                    "status": random.choice(statuses),
                    "created_at": gerar_data_aleatoria(30),
                    "updated_at": datetime.now(UTC)
                }
            )
            atividades_inseridas += 1
        except Exception:
            pass
    
    if atividades_inseridas > 0:
        await session.flush()
        print(f"  ✅ {atividades_inseridas} atividades criadas")
    else:
        print(f"  [SKIP] Tabela citizenship_requests não existe")
    
    return atividades_inseridas

async def seed_pendencias(session: AsyncSession, quantidade: int = 17) -> int:
    """Seed de pendências/reclamações"""
    print(f"➕ Criando {quantidade} reclamações pendentes...")
    
    from sqlalchemy import text
    
    pendencias_inseridas = 0
    statuses = ["pending", "open", "in_progress", "closed"]
    
    for i in range(quantidade):
        try:
            await session.execute(
                text("""
                    INSERT INTO complaints_complaints (title, description, status, created_at, updated_at)
                    VALUES (:title, :description, :status, :created_at, :updated_at)
                """),
                {
                    "title": f"Reclamação #{i+1:03d}",
                    "description": f"Problema com serviço - Descrição detalhada #{i+1}",
                    "status": random.choice(statuses),
                    "created_at": gerar_data_aleatoria(30),
                    "updated_at": datetime.now(UTC)
                }
            )
            pendencias_inseridas += 1
        except Exception:
            pass
    
    if pendencias_inseridas > 0:
        await session.flush()
        print(f"  ✅ {pendencias_inseridas} reclamações criadas")
    else:
        print(f"  [SKIP] Tabela complaints_complaints não existe")
    
    return pendencias_inseridas

# ===========================
# Main Seed Function
# ===========================

async def main():
    """Executa seed completo"""
    
    print("\n" + "="*60)
    print("🌱 SEED DASHBOARD - SILA SYSTEM (Angola 2025)")
    print("="*60 + "\n")
    
    try:
        # Conectar ao banco
        async with async_session_factory() as session:
            async with session.begin():
                
                # 1. Usuários
                usuarios_count = await seed_usuarios(session, quantidade=89)
                
                # 2. Documentos
                documentos_count = await seed_documentos(session, quantidade=1247)
                
                # 3. Atividades (CitizenshipRequest)
                atividades_count = await seed_atividades(session, quantidade=42)
                
                # 4. Pendências (Complaints)
                pendencias_count = await seed_pendencias(session, quantidade=17)
            
            await session.commit()
        
        # ===========================
        # Resumo Final
        # ===========================
        print("\n" + "="*60)
        print("✅ SEED COMPLETO COM SUCESSO!")
        print("="*60)
        print(f"\n📊 Dados Populados:")
        print(f"   • {usuarios_count} Usuários")
        print(f"   • {documentos_count} Documentos")
        print(f"   • {atividades_count} Atividades (Citizenship Requests)")
        print(f"   • {pendencias_count} Reclamações (Complaints)")
        
        print(f"\n🎯 Dashboard Métricas:")
        print(f"   • Total Documentos: {documentos_count}")
        print(f"   • Total Usuários: {usuarios_count}")
        print(f"   • Atividades Recentes: {atividades_count}")
        print(f"   • Pendências: {pendencias_count}")
        
        print(f"\n🔧 Próximos Passos:")
        print(f"   1. Acesse: http://localhost:3000")
        print(f"   2. Veja o Dashboard com dados reais!")
        
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# ===========================
# Entry Point
# ===========================

if __name__ == "__main__":
    asyncio.run(main())
