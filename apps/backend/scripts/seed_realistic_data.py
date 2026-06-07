"""Seed realistic public services for operational citizen flow."""

from __future__ import annotations

import asyncio
from decimal import Decimal

from sqlalchemy import select

from apps.backend.app.core.catalog.models.service import Service
from apps.backend.app.core.db import AsyncSessionLocal

SEED_SERVICES = [
    {
        "code": "CERTIDAO_NASCIMENTO",
        "name": "Emissão de Certidão de Nascimento",
        "price": Decimal("2500.00"),
        "estimated_days": 3,
        "icon_slug": "certificate",
    },
    {
        "code": "CERTIDAO_CASAMENTO",
        "name": "Emissão de Certidão de Casamento",
        "price": Decimal("3000.00"),
        "estimated_days": 4,
        "icon_slug": "marriage",
    },
    {
        "code": "ATESTADO_RESIDENCIA",
        "name": "Emissão de Atestado de Residência",
        "price": Decimal("1500.00"),
        "estimated_days": 2,
        "icon_slug": "address",
    },
]


async def seed_services() -> None:
    async with AsyncSessionLocal() as session:
        for item in SEED_SERVICES:
            existing = (
                (await session.execute(select(Service).where(Service.code == item["code"])))
                .scalars()
                .first()
            )
            if existing:
                existing.name = item["name"]
                existing.price = item["price"]
                existing.estimated_days = item["estimated_days"]
                existing.is_active = True
                existing.scope = "public"
                existing.is_public = True
                existing.is_essential = True
                existing.icon_slug = item["icon_slug"]
                continue

            session.add(
                Service(
                    code=item["code"],
                    name=item["name"],
                    scope="public",
                    is_active=True,
                    is_public=True,
                    is_essential=True,
                    price=item["price"],
                    estimated_days=item["estimated_days"],
                    icon_slug=item["icon_slug"],
                )
            )

        await session.commit()
        print(f"Seeded {len(SEED_SERVICES)} realistic services")


if __name__ == "__main__":
    asyncio.run(seed_services())
