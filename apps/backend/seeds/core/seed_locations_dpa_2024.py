#!/usr/bin/env python3
"""
Seed locations (PROVINCIA/MUNICIPIO/COMUNA) com base no DPA 2024.

Uso:
  PYTHONPATH=apps/backend python apps/backend/seeds/core/seed_locations_dpa_2024.py
  PYTHONPATH=apps/backend python apps/backend/seeds/core/seed_locations_dpa_2024.py --check
"""

import argparse
import asyncio
import logging
import os
from pathlib import Path
from typing import Dict, Tuple
import importlib.util

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

DB_USER = os.getenv("POSTGRES_USER", "sila_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Trumanmarcelo_1983")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "sila_db")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async def _get_or_create_location(
    session: AsyncSession,
    *,
    name: str,
    territory_type: str,
    parent_id,
) -> Tuple[str, str]:
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


def _load_angola_dpa() -> Dict[str, Dict[str, Dict[str, list]]]:
    seed_path = Path("docs/seed_angola_dpa_2024.cpython-312.pyc")
    if not seed_path.exists():
        raise RuntimeError("Arquivo seed_angola_dpa_2024.cpython-312.pyc não encontrado em docs/")

    spec = importlib.util.spec_from_file_location("seed_angola_dpa_2024_docs", seed_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    data = getattr(module, "ANGOLA_DPA", None) or getattr(module, "ANGOLA_DPA_2024", None)
    if data is None:
        raise RuntimeError("ANGOLA_DPA não encontrado no arquivo .pyc")
    return data.get("ANGOLA", {}) if isinstance(data, dict) and "ANGOLA" in data else data


def _normalize_province_name(name: str) -> str:
    normalized = name.strip()
    lowered = normalized.lower()
    if lowered == "cuando cubango":
        return "Cubango"
    if lowered == "icolo e bengo":
        return "Icolo e Bengo"
    return normalized


async def seed_locations(session: AsyncSession, *, reset: bool = False) -> Dict[str, int]:
    angola_dpa = _load_angola_dpa()
    logger.info("🌍 Iniciando seed completo DPA 2024 para locations...")
    territory_ids = {}

    if reset:
        logger.warning("⚠️ Reset ativo: limpando locations (PROVINCIA/MUNICIPIO/COMUNA) com CASCADE.")
        await session.execute(
            text("TRUNCATE locations CASCADE")
        )
        await session.commit()

    # 1) Provincias
    for province_name in angola_dpa.keys():
        province_name = _normalize_province_name(province_name)
        row = await _get_or_create_location(
            session,
            name=province_name,
            territory_type="PROVINCIA",
            parent_id=None,
        )
        if row:
            location_id, name = row
            territory_ids[(name, "PROVINCIA")] = location_id

    # 2) Municipios
    for province_name, municipalities in angola_dpa.items():
        province_name = _normalize_province_name(province_name)
        parent_id = territory_ids.get((province_name, "PROVINCIA"))
        if not parent_id:
            logger.warning("⚠️ Província '%s' não encontrada.", province_name)
            continue

        for municipality_name in municipalities.keys():
            row = await _get_or_create_location(
                session,
                name=municipality_name.title() if municipality_name.isupper() else municipality_name,
                territory_type="MUNICIPIO",
                parent_id=parent_id,
            )
            if row:
                location_id, name = row
                territory_ids[(province_name, name, "MUNICIPIO")] = location_id

    # 3) Comunas
    for province_name, municipalities in angola_dpa.items():
        province_name = _normalize_province_name(province_name)
        for municipality_name, communes in municipalities.items():
            mun_key = municipality_name.title() if municipality_name.isupper() else municipality_name
            parent_id = territory_ids.get((province_name, mun_key, "MUNICIPIO"))
            if not parent_id:
                logger.warning(
                    "⚠️ Município '%s' da província '%s' não encontrado.",
                    mun_key,
                    province_name,
                )
                continue
            for commune_name in communes:
                await _get_or_create_location(
                    session,
                    name=commune_name,
                    territory_type="COMUNA",
                    parent_id=parent_id,
                )

    await session.commit()

    stats = {}
    for t in ("PROVINCIA", "MUNICIPIO", "COMUNA"):
        result = await session.execute(
            text("SELECT COUNT(*) FROM locations WHERE type = :type"),
            {"type": t},
        )
        stats[t.lower()] = result.scalar() or 0

    return stats


async def check_counts(session: AsyncSession) -> Dict[str, int]:
    stats = {}
    for t in ("PROVINCIA", "MUNICIPIO", "COMUNA"):
        result = await session.execute(
            text("SELECT COUNT(*) FROM locations WHERE type = :type"),
            {"type": t},
        )
        stats[t.lower()] = result.scalar() or 0
    return stats


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Apenas validar contagens")
    parser.add_argument("--reset", action="store_true", help="Limpa locations antes de popular")
    args = parser.parse_args()

    engine = create_async_engine(DATABASE_URL)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        if args.check:
            stats = await check_counts(session)
            logger.info("📊 Contagens atuais: %s", stats)
        else:
            stats = await seed_locations(session, reset=args.reset)
            logger.info("✅ Seed concluído. Contagens: %s", stats)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
