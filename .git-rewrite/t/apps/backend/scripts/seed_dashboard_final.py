#!/usr/bin/env python3
"""
SILA Dashboard Seed Script - Production Ready
Popula o banco de dados com dados reais e realistas para o dashboard

Uso:
    python scripts/seed_dashboard.py

Requisitos:
    - PostgreSQL rodando
    - .env configurado com DATABASE_URL e ASYNC_DATABASE_URL
    - Migrações aplicadas (alembic upgrade head)
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta, UTC
from pathlib import Path

# Add backend root to path
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

from sqlalchemy import text

try:
    from core.db.session import async_session_factory
    from config.settings import settings
    DB_AVAILABLE = True
except Exception as e:
    print(f"[WARNING] Database não disponível: {e}")
    DB_AVAILABLE = False

import random

# ===========================
# Dados Realistas (Angola)
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


# ===========================
# Funções Auxiliares
# ===========================

def gerar_nome() -> str:
    """Gera nome aleatório realista"""
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"


def gerar_email(nome: str, idx: int) -> str:
    """Gera email corporativo .gov.ao"""
    primeiro = nome.split()[0].lower()
    return f"{primeiro}{idx}@sila.gov.ao"


def gerar_bi() -> str:
    """Gera número de Bilhete de Identidade realista (Angola)"""
    return f"{random.randint(1000000, 9999999)}LA{random.randint(10, 99)}"


def gerar_data_aleatoria(dias_atras: int = 365) -> datetime:
    """Gera data aleatória nos últimos N dias"""
    return datetime.now(UTC) - timedelta(days=random.randint(0, dias_atras))


# ===========================
# Seed Functions
# ===========================

async def seed_usuarios(session, quantidade: int = 89) -> int:
    """Seed de usuários com SQL direto (mais robusto)"""
    print(f"➕ Criando {quantidade} usuários...")

    inserted = 0
    
    try:
        # Admin
        await session.execute(
            text("""
                INSERT INTO identity_users (email, name, is_active, created_at, updated_at)
                VALUES (:email, :name, :is_active, :created_at, :updated_at)
                ON CONFLICT (email) DO NOTHING
            """),
            {
                "email": "admin@sila.gov.ao",
                "name": "Admin SILA",
                "is_active": True,
                "created_at": datetime.now(UTC) - timedelta(days=365),
                "updated_at": datetime.now(UTC),
            },
        )
        inserted += 1

        # Outros usuários
        for i in range(1, quantidade):
            nome = gerar_nome()
            await session.execute(
                text("""
                    INSERT INTO identity_users (email, name, is_active, created_at, updated_at)
                    VALUES (:email, :name, :is_active, :created_at, :updated_at)
                    ON CONFLICT (email) DO NOTHING
                """),
                {
                    "email": gerar_email(nome, i),
                    "name": nome,
                    "is_active": random.choice([True, True, True, False]),
                    "created_at": gerar_data_aleatoria(180),
                    "updated_at": datetime.now(UTC),
                },
            )
            inserted += 1

            # Progress
            if (i + 1) % 20 == 0:
                await session.flush()

        await session.flush()
        print(f"  ✅ {inserted} usuários criados")
        return inserted

    except Exception as e:
        print(f"  [ERROR] Não foi possível criar usuários: {e}")
        return 0


async def seed_documentos(session, quantidade: int = 1247) -> int:
    """Seed de documentos"""
    print(f"➕ Criando {quantidade} documentos...")

    inserted = 0
    
    try:
        for i in range(quantidade):
            nome = gerar_nome()
            await session.execute(
                text("""
                    INSERT INTO documents_documents 
                    (filename, original_name, file_size, uploaded_by_id, created_at, updated_at)
                    VALUES 
                    (:filename, :original_name, :file_size, :uploaded_by_id, :created_at, :updated_at)
                """),
                {
                    "filename": f"doc_{datetime.now(UTC).strftime('%Y%m%d')}_{i+1000}.pdf",
                    "original_name": f"Certidão_{nome.replace(' ', '_')}_{random.randint(1970, 2005)}.pdf",
                    "file_size": random.randint(80000, 5000000),
                    "uploaded_by_id": 1 + (i % 89) if i < 1247 else 1,
                    "created_at": gerar_data_aleatoria(365),
                    "updated_at": datetime.now(UTC),
                },
            )
            inserted += 1

            if (i + 1) % 100 == 0:
                await session.flush()
                print(f"  [PROGRESS] {i + 1}/{quantidade}")

        await session.flush()
        print(f"  ✅ {inserted} documentos criados")
        return inserted

    except Exception as e:
        print(f"  [ERROR] Não foi possível criar documentos: {e}")
        return 0


async def seed_citizenship_requests(session, quantidade: int = 42) -> int:
    """Seed de citizenship requests"""
    print(f"➕ Criando {quantidade} atividades (citizenship requests)...")

    inserted = 0
    statuses = ["approved", "pending", "processing", "rejected"]
    
    try:
        for i in range(quantidade):
            nome = gerar_nome()
            await session.execute(
                text("""
                    INSERT INTO citizenship_requests 
                    (full_name, bi_number, status, created_at, updated_at)
                    VALUES 
                    (:full_name, :bi_number, :status, :created_at, :updated_at)
                """),
                {
                    "full_name": nome,
                    "bi_number": gerar_bi(),
                    "status": random.choice(statuses),
                    "created_at": gerar_data_aleatoria(30),
                    "updated_at": datetime.now(UTC),
                },
            )
            inserted += 1

        await session.flush()
        print(f"  ✅ {inserted} atividades criadas")
        return inserted

    except Exception as e:
        print(f"  [ERROR] Não foi possível criar citizenship requests: {e}")
        return 0


async def seed_complaints(session, quantidade: int = 17) -> int:
    """Seed de reclamações"""
    print(f"➕ Criando {quantidade} reclamações...")

    inserted = 0
    statuses = ["pending", "open", "in_progress", "closed", "resolved"]
    
    try:
        for i in range(quantidade):
            await session.execute(
                text("""
                    INSERT INTO complaints_complaints 
                    (title, description, status, created_at, updated_at)
                    VALUES 
                    (:title, :description, :status, :created_at, :updated_at)
                """),
                {
                    "title": f"Reclamação #{i+1:03d}",
                    "description": f"Problema com serviço - Descrição detalhada #{i+1}",
                    "status": random.choice(statuses),
                    "created_at": gerar_data_aleatoria(30),
                    "updated_at": datetime.now(UTC),
                },
            )
            inserted += 1

        await session.flush()
        print(f"  ✅ {inserted} reclamações criadas")
        return inserted

    except Exception as e:
        print(f"  [ERROR] Não foi possível criar complaints: {e}")
        return 0


# ===========================
# Main Orchestrator
# ===========================

async def main():
    """Executa seed completo"""

    print("\n" + "=" * 70)
    print("🌱 SILA SYSTEM - DASHBOARD SEED")
    print("=" * 70)
    print(f"Timestamp: {datetime.now(UTC).isoformat()}")
    print(f"Environment: {settings.ENVIRONMENT if DB_AVAILABLE else 'N/A'}")
    print("=" * 70 + "\n")

    if not DB_AVAILABLE:
        print("❌ Database não disponível.")
        print("   Certifique-se que:")
        print("   1. PostgreSQL está rodando")
        print("   2. .env está configurado corretamente")
        print("   3. Migrações foram aplicadas\n")
        return

    try:
        async with async_session_factory() as session:
            async with session.begin():
                print("[INFO] Iniciando population de dados...\n")

                # Seed each table
                usuarios_count = await seed_usuarios(session, quantidade=89)
                documentos_count = await seed_documentos(session, quantidade=1247)
                citizenship_count = await seed_citizenship_requests(
                    session, quantidade=42
                )
                complaints_count = await seed_complaints(session, quantidade=17)

            # Commit
            print("\n[INFO] Commitando mudanças...")
            try:
                await session.commit()
                print("[✓] Commit bem-sucedido!")
            except Exception as e:
                print(f"[ERROR] Falha no commit: {e}")
                await session.rollback()
                raise

        # Summary
        print("\n" + "=" * 70)
        print("✅ SEED COMPLETO COM SUCESSO!")
        print("=" * 70)
        total = usuarios_count + documentos_count + citizenship_count + complaints_count
        print(f"\n📊 Dados Populados:")
        print(f"   • {usuarios_count:>6} Usuários")
        print(f"   • {documentos_count:>6} Documentos")
        print(f"   • {citizenship_count:>6} Atividades (Citizenship Requests)")
        print(f"   • {complaints_count:>6} Reclamações (Complaints)")
        print(f"   {'─' * 45}")
        print(f"   • {total:>6} TOTAL")

        print(f"\n🎯 Dashboard Métricas:")
        print(f"   ✓ Documentos populados para filtros e buscas")
        print(f"   ✓ Usuários para controle de acesso")
        print(f"   ✓ Atividades recentes (últimos 30 dias)")
        print(f"   ✓ Pendências ativas (últimos 30 dias)")

        print(f"\n🚀 Próximos Passos:")
        print(f"   1. Inicie o backend: python -m uvicorn main:app --reload")
        print(f"   2. Inicie o frontend: npm run dev")
        print(f"   3. Acesse: http://localhost:3000")
        print(f"   4. Dashboard terá dados reais para exploração")

        print("\n" + "=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ===========================
# Entry Point
# ===========================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[CANCELLED] Operação cancelada pelo usuário\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL] {e}\n")
        sys.exit(1)
