#!/usr/bin/env python3
"""
🎯 MASTER SEED - SILA SYSTEM (Lei 14/24)

CONSOLIDAÇÃO ÚNICA DE SEEDS - Substitui todos os 26 scripts anteriores

Funcionalidades:
1. ✅ Lei 14/24 - 21 Províncias + 6 Municípios + 5 Comunas
2. ✅ Usuários por Níveis - 5 níveis administrativos
3. ✅ Seed Institucional Educação - anos/escolas/turmas
4. ✅ Cidadãos de Teste - 3 exemplos com vinculação territorial
5. ✅ Seed de Finanças - faturas/pagamentos mínimos para dashboard
6. ✅ Validação Final - Integridade referencial

Uso:
  python run_master_seed.py              # Executa tudo
  python run_master_seed.py --territories-only
  python run_master_seed.py --users-only
  python run_master_seed.py --check
"""

import argparse
import asyncio
import logging
import os
import sys
import json
from pathlib import Path
from uuid import uuid4
import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Garantir import absoluto de módulos irmãos (ex.: scripts.seed_educacao_institucional)
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURAÇÃO DO BANCO
# ============================================================================

DB_USER = os.getenv("POSTGRES_USER", "sila_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Trumanmarcelo_1983")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "sila_db")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Senha universal de teste
TEST_PASSWORD = "SilaSystem_2026"

# ============================================================================
# 1. SEED DE TERRITÓRIOS (Lei 14/24)
# ============================================================================

PROVINCES = {
    "Cabinda": None,
    "Zaire": None,
    "Uíge": None,
    "Bengo": None,
    "Cuanza-Norte": None,
    "Cuanza-Sul": None,
    "Huambo": None,
    "Benguela": None,
    "Huíla": None,
    "Namibe": None,
    "Cunene": None,
    "Moxico": None,
    "Malanje": None,
    "Lunda-Norte": None,
    "Lunda-Sul": None,
    "Bié": None,
    "Luanda": None,
    "Icolo e Bengo": None,
    "Moxico Leste": None,
    "Cuando": None,
    "Cubango": None,
}

MUNICIPALITIES = {
    "Huambo": ["Huambo (Município)", "Bailundo", "Longonjo"],
    "Luanda": ["Luanda (Município)", "Cacuaco", "Viana"],
}

COMMUNES = {
    "Huambo (Município)": ["Comuna Centro", "Comuna Norte", "Comuna Sul"],
    "Bailundo": ["Bailundo Centro", "Bailundo Rural"],
}

async def _get_or_create_location(
    session: AsyncSession,
    *,
    name: str,
    territory_type: str,
    parent_id,
):
    """Resolve localização existente ou cria uma nova de forma idempotente.

    Não depende de um target fixo de ON CONFLICT, porque ambientes legados
    podem ter constraints diferentes em `locations`.
    """
    if parent_id is None:
        existing = await session.execute(
            text(
                """
                SELECT id, name
                FROM locations
                WHERE name = :name
                  AND type = :type
                  AND parent_id IS NULL
                LIMIT 1
                """
            ),
            {"name": name, "type": territory_type},
        )
    else:
        existing = await session.execute(
            text(
                """
                SELECT id, name
                FROM locations
                WHERE name = :name
                  AND type = :type
                  AND parent_id = :parent
                LIMIT 1
                """
            ),
            {"name": name, "type": territory_type, "parent": parent_id},
        )
    row = existing.fetchone()
    if row:
        return row

    # Fallback para ambientes com unicidade global (name, type),
    # sem diferenciar parent_id.
    existing_by_name_type = await session.execute(
        text(
            """
            SELECT id, name
            FROM locations
            WHERE name = :name
              AND type = :type
            LIMIT 1
            """
        ),
        {"name": name, "type": territory_type},
    )
    row = existing_by_name_type.fetchone()
    if row:
        return row

    inserted = await session.execute(
        text(
            """
            INSERT INTO locations (name, type, parent_id)
            VALUES (:name, :type, :parent)
            RETURNING id, name
            """
        ),
        {"name": name, "type": territory_type, "parent": parent_id},
    )
    return inserted.fetchone()

async def seed_territories(session: AsyncSession) -> dict:
    """Insere territórios com UPSERT idempotente"""
    logger.info("🌍 Iniciando seed de territórios Lei 14/24...")
    
    territory_ids = {}
    
    try:
        # 1️⃣ PROVÍNCIAS
        logger.info("📍 Inserindo 21 províncias...")
        for province_name in PROVINCES.keys():
            row = await _get_or_create_location(
                session,
                name=province_name,
                territory_type="PROVINCIA",
                parent_id=None,
            )
            if row:
                location_id, name = row
                territory_ids[name] = location_id
                logger.info(f"   ✅ {name:25s} (ID: {location_id})")
        
        # 2️⃣ MUNICÍPIOS
        logger.info("📍 Inserindo 6 municípios...")
        for province_name, municipalities in MUNICIPALITIES.items():
            parent_id = territory_ids.get(province_name)
            if not parent_id:
                logger.warning(f"   ⚠️ Província '{province_name}' não encontrada!")
                continue
            
            for mun_name in municipalities:
                row = await _get_or_create_location(
                    session,
                    name=mun_name,
                    territory_type="MUNICIPIO",
                    parent_id=parent_id,
                )
                if row:
                    location_id, name = row
                    territory_ids[name] = location_id
                    logger.info(f"   ✅ {name:25s} (ID: {location_id})")
        
        # 3️⃣ COMUNAS
        logger.info("📍 Inserindo 5 comunas...")
        for mun_name, communes in COMMUNES.items():
            parent_id = territory_ids.get(mun_name)
            if not parent_id:
                logger.warning(f"   ⚠️ Município '{mun_name}' não encontrado!")
                continue
            
            for comm_name in communes:
                row = await _get_or_create_location(
                    session,
                    name=comm_name,
                    territory_type="COMUNA",
                    parent_id=parent_id,
                )
                if row:
                    location_id, name = row
                    territory_ids[name] = location_id
                    logger.info(f"   ✅ {name:25s} (ID: {location_id})")
        
        await session.commit()
        logger.info(f"✅ Seed de territórios completo: {len(territory_ids)} registros\n")
        return territory_ids
    
    except Exception as e:
        logger.error(f"❌ Erro ao fazer seed de territórios: {e}")
        await session.rollback()
        raise

# ============================================================================
# 2. SEED DE USUÁRIOS (5 NÍVEIS)
# ============================================================================

async def seed_users(session: AsyncSession, territory_ids: dict) -> None:
    """Insere usuários por níveis administrativos"""
    logger.info("👥 Iniciando seed de usuários (5 níveis)...")
    
    users_config = [
        {
            "email": "admin@sila.gov.ao",
            "full_name": "Administrator SILA",
            "level": "SUPER",
            "region_id": None,
        },
        {
            "email": "provincial.luanda@sila.gov.ao",
            "full_name": "Provincial Manager - Luanda",
            "level": "PROVINCIAL",
            "region_name": "Luanda",
        },
        {
            "email": "provincial.huambo@sila.gov.ao",
            "full_name": "Provincial Manager - Huambo",
            "level": "PROVINCIAL",
            "region_name": "Huambo",
        },
        {
            "email": "municipal.huambo@sila.gov.ao",
            "full_name": "Municipal Manager - Huambo",
            "level": "MUNICIPAL",
            "region_name": "Huambo (Município)",
        },
        {
            "email": "commune.center.huambo@sila.gov.ao",
            "full_name": "Commune Officer - Centro (Huambo)",
            "level": "COMMUNAL",
            "region_name": "Comuna Centro",
        },
    ]
    
    created_count = 0
    skipped_count = 0
    unresolved_regions = 0

    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    async def _ensure_role(role_name: str) -> str:
        role_result = await session.execute(
            text("SELECT id FROM iam_roles WHERE name = :name"),
            {"name": role_name},
        )
        row = role_result.fetchone()
        if row:
            return row[0]
        role_id = str(uuid4())
        await session.execute(
            text(
                """
                INSERT INTO iam_roles (
                    id, name, description, role_type, is_system, created_at, is_active
                ) VALUES (
                    :id, :name, :description, :role_type, :is_system, now(), :is_active
                )
                """
            ),
            {
                "id": role_id,
                "name": role_name,
                "description": f"Seed role: {role_name}",
                "role_type": "SYSTEM",
                "is_system": True,
                "is_active": True,
            },
        )
        return role_id

    try:
        for user_config in users_config:
            # Resolver region_id
            region_id = user_config.get("region_id")
            if "region_name" in user_config:
                region_id = territory_ids.get(user_config["region_name"])
                if not region_id:
                    logger.error(
                        "   ❌ %s: território '%s' não encontrado",
                        user_config["email"],
                        user_config["region_name"],
                    )
                    unresolved_regions += 1
                    continue
            
            role_names = ["SUPERADMIN"] if user_config["level"] == "SUPER" else ["MANAGER"]
            role_ids = [await _ensure_role(role) for role in role_names]

            metadata = {
                "administrative_level": user_config["level"],
                "region_id": str(region_id) if region_id else None,
                "region_name": user_config.get("region_name"),
            }

            check_result = await session.execute(
                text("SELECT id FROM iam_users WHERE email = :email"),
                {"email": user_config["email"]},
            )
            existing = check_result.fetchone()

            try:
                if existing:
                    user_id = existing[0]
                    await session.execute(
                        text(
                            """
                            UPDATE iam_users
                            SET username = :username,
                                password_hash = :password_hash,
                                full_name = :full_name,
                                status = :status,
                                is_active = true,
                                custom_metadata = :custom_metadata
                            WHERE id = :id
                            """
                        ),
                        {
                            "id": user_id,
                            "username": user_config["email"],
                            "password_hash": _hash_password(TEST_PASSWORD),
                            "full_name": user_config["full_name"],
                            "status": "ACTIVE",
                            "custom_metadata": json.dumps(metadata),
                        },
                    )
                    logger.info(f"   ⏭️  {user_config['email']:40s} (atualizado)")
                    skipped_count += 1
                else:
                    user_id = str(uuid4())
                    await session.execute(
                        text(
                            """
                            INSERT INTO iam_users (
                                id, username, email, password_hash, status,
                                is_superuser, full_name, created_at, is_active,
                                custom_metadata
                            ) VALUES (
                                :id, :username, :email, :password_hash, :status,
                                :is_superuser, :full_name, now(), true,
                                :custom_metadata
                            )
                            """
                        ),
                        {
                            "id": user_id,
                            "username": user_config["email"],
                            "email": user_config["email"],
                            "password_hash": _hash_password(TEST_PASSWORD),
                            "status": "ACTIVE",
                            "is_superuser": user_config["level"] == "SUPER",
                            "full_name": user_config["full_name"],
                            "custom_metadata": json.dumps(metadata),
                        },
                    )
                    logger.info(f"   ✅ {user_config['email']:40s} ({user_config['level']})")
                    created_count += 1

                for role_id in role_ids:
                    await session.execute(
                        text(
                            """
                            INSERT INTO iam_user_roles (id, user_id, role_id, assigned_at, is_active)
                            VALUES (:id, :user_id, :role_id, now(), true)
                            ON CONFLICT (user_id, role_id) DO NOTHING
                            """
                        ),
                        {
                            "id": str(uuid4()),
                            "user_id": user_id,
                            "role_id": role_id,
                        },
                    )

            except Exception as e:
                logger.error(f"   ❌ {user_config['email']:40s} ERRO: {e}")

        if unresolved_regions:
            raise RuntimeError(
                f"{unresolved_regions} usuário(s) sem território resolvido. "
                "Execute seed de territórios antes de --users-only."
            )
        
        await session.commit()
        logger.info(f"✅ Seed de usuários completo: {created_count} criados, {skipped_count} já existentes\n")
    
    except Exception as e:
        logger.error(f"❌ Erro ao fazer seed de usuários: {e}")
        await session.rollback()
        raise

# ============================================================================
# 3. SEED EDUCAÇÃO INSTITUCIONAL
# ============================================================================

async def seed_educacao_institucional() -> dict[str, int]:
    """Executa seed institucional de educação no fluxo mestre."""
    logger.info("🏫 Iniciando seed institucional de educação...")
    from scripts.seed_educacao_institucional import seed as seed_educacao

    result = await seed_educacao(dry_run=False)
    logger.info(
        "✅ Educação: anos(c=%s,u=%s), escolas(c=%s,u=%s), turmas(c=%s,u=%s)\n",
        result["created_anos"],
        result["updated_anos"],
        result["created_escolas"],
        result["updated_escolas"],
        result["created_turmas"],
        result["updated_turmas"],
    )
    return result

# ============================================================================
# 4. SEED DE FINANÇAS (DASHBOARD)
# ============================================================================

async def seed_financas_dashboard() -> None:
    """Executa seed mínimo de faturas/pagamentos para dashboard."""
    logger.info("💰 Iniciando seed de finanças (dashboard)...")
    from scripts.seed_financas_dashboard import seed_financas_dashboard as seed_financas

    await seed_financas()
    logger.info("✅ Finanças: seed mínimo concluído\n")

# ============================================================================
# 5. RESOLUÇÃO TERRITORIAL (SUPORTE USERS-ONLY)
# ============================================================================

async def load_territory_ids(session: AsyncSession) -> dict:
    """Carrega mapa name -> id para territórios já existentes."""
    result = await session.execute(
        text(
            """
            SELECT id, name
            FROM locations
            WHERE type IN ('PROVINCIA', 'MUNICIPIO', 'COMUNA')
            """
        )
    )
    rows = result.fetchall()
    return {row[1]: row[0] for row in rows}

# ============================================================================
# 6. VALIDAÇÃO FINAL
# ============================================================================

async def validate_data(
    session: AsyncSession,
    *,
    require_territories: bool = True,
    require_users: bool = True,
) -> bool:
    """Valida integridade dos dados inseridos por modo de execução."""
    logger.info("✓ Validando integridade dos dados...")
    
    try:
        # Contar territórios
        result = await session.execute(text("SELECT COUNT(*) FROM locations WHERE type = 'PROVINCIA'"))
        provinces = result.scalar() or 0
        
        result = await session.execute(text("SELECT COUNT(*) FROM locations WHERE type = 'MUNICIPIO'"))
        municipalities = result.scalar() or 0
        
        result = await session.execute(text("SELECT COUNT(*) FROM locations WHERE type = 'COMUNA'"))
        communes = result.scalar() or 0
        
        result = await session.execute(text("SELECT COUNT(*) FROM iam_users"))
        users = result.scalar() or 0
        
        logger.info(f"   📊 Territórios: {provinces} províncias, {municipalities} municípios, {communes} comunas")
        logger.info(f"   👥 Usuários: {users}")
        
        # Validações
        success = True
        if require_territories and provinces < 21:
            logger.warning(f"   ⚠️ Esperado 21 províncias, encontrado {provinces}")
            success = False
        
        if require_territories and municipalities < 6:
            logger.warning(f"   ⚠️ Esperado 6 municípios, encontrado {municipalities}")
            success = False
        
        if require_territories and communes < 5:
            logger.warning(f"   ⚠️ Esperado 5 comunas, encontrado {communes}")
            success = False
        
        if require_users and users == 0:
            logger.warning("   ⚠️ Nenhum usuário encontrado!")
            success = False
        
        if success:
            logger.info("✅ Validação concluída com sucesso!\n")
        
        return success
    
    except Exception as e:
        logger.error(f"❌ Erro na validação: {e}")
        return False

# ============================================================================
# 7. CLI
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Master seed do SILA System.")
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--territories-only",
        action="store_true",
        help="Executa apenas seed de territórios e valida territórios.",
    )
    mode_group.add_argument(
        "--users-only",
        action="store_true",
        help="Executa apenas seed de usuários (requer territórios já existentes).",
    )
    mode_group.add_argument(
        "--check",
        action="store_true",
        help="Não altera dados; apenas valida integridade atual.",
    )
    return parser.parse_args()

# ============================================================================
# 8. MAIN
# ============================================================================

async def main():
    """Executa o seed completo"""
    args = parse_args()

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🎯 MASTER SEED - SILA SYSTEM (Lei 14/24)                       ║
║                  Consolidação Única de Todos os Seeds                     ║
║                                                                            ║
║         Credenciais: sila_user / Trumanmarcelo_1983                       ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    
    engine = create_async_engine(DATABASE_URL, echo=False)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    try:
        async with AsyncSessionLocal() as session:
            if args.check:
                logger.info("🔎 Modo CHECK: sem escrita no banco.")
                ok = await validate_data(
                    session,
                    require_territories=True,
                    require_users=True,
                )
                if ok:
                    logger.info("✅ CHECK concluído com sucesso!")
                    return 0
                logger.error("❌ CHECK encontrou inconsistências")
                return 1

            if args.territories_only:
                logger.info("🧭 Modo TERRITORIES-ONLY")
                await seed_territories(session)
                await seed_financas_dashboard()
                ok = await validate_data(
                    session,
                    require_territories=True,
                    require_users=False,
                )
                if ok:
                    logger.info("✅ TERRITORIES-ONLY concluído com sucesso!")
                    return 0
                logger.error("❌ TERRITORIES-ONLY com falhas de validação")
                return 1

            if args.users_only:
                logger.info("👤 Modo USERS-ONLY")
                territory_ids = await load_territory_ids(session)
                await seed_users(session, territory_ids)
                await seed_financas_dashboard()
                ok = await validate_data(
                    session,
                    require_territories=False,
                    require_users=True,
                )
                if ok:
                    logger.info("✅ USERS-ONLY concluído com sucesso!")
                    return 0
                logger.error("❌ USERS-ONLY com falhas de validação")
                return 1

            # Fluxo completo padrão
            territory_ids = await seed_territories(session)
            await seed_users(session, territory_ids)
            await seed_educacao_institucional()
            await seed_financas_dashboard()
            ok = await validate_data(
                session,
                require_territories=True,
                require_users=True,
            )
            if ok:
                logger.info("🎉 SEED COMPLETO COM SUCESSO!")
                return 0
            logger.error("❌ SEED COM FALHAS")
            return 1
    
    except Exception as e:
        logger.error(f"❌ Erro crítico: {e}")
        return 1
    
    finally:
        await engine.dispose()

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
