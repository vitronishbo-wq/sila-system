#!/usr/bin/env python3
"""Seed 50+ modules and 900+ configurable services in the catalog."""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections.abc import Iterable
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from apps.backend.app.core.catalog.blueprint import (  # noqa: E402
    MODULE_BLUEPRINTS,
    build_service_blueprints,
)
from apps.backend.app.core.catalog.models.module import Module  # noqa: E402
from apps.backend.app.core.catalog.models.service import Service  # noqa: E402
from apps.backend.app.core.db import AsyncSessionLocal  # noqa: E402

SERVICE_COLUMNS = set(Service.__table__.columns.keys())


def _chunk(items: list[str], size: int = 250) -> Iterable[list[str]]:
    for idx in range(0, len(items), size):
        yield items[idx : idx + size]


def _service_create_data(item: dict, module_id: int) -> dict:
    data = {
        "code": item["code"],
        "name": item["name"],
        "scope": "public" if item["visibility"] == "PUBLIC" else "internal",
        "is_active": True,
        "module_id": module_id,
        "price": item["fee"],
        "estimated_days": item["sla_days"],
        "is_public": item["visibility"] == "PUBLIC",
        "is_essential": item["is_essential"],
        "icon_slug": item["module_slug"],
    }

    optional = {
        "description": item["description"],
        "workflow_definition_key": item["workflow_template"],
        "required_documents": list(item["required_documents"]),
        "visibility": item["visibility"],
        "version": 1,
        "business_priority": item["business_priority"],
    }
    for key, value in optional.items():
        if key in SERVICE_COLUMNS:
            data[key] = value
    return data


def _apply_service_update(service: Service, item: dict, module_id: int) -> None:
    service.name = item["name"]
    service.scope = "public" if item["visibility"] == "PUBLIC" else "internal"
    service.is_active = True
    service.module_id = module_id
    service.price = Decimal(item["fee"])
    service.estimated_days = int(item["sla_days"])
    service.is_public = item["visibility"] == "PUBLIC"
    service.is_essential = item["is_essential"]
    service.icon_slug = item["module_slug"]

    if "description" in SERVICE_COLUMNS:
        service.description = item["description"]
    if "workflow_definition_key" in SERVICE_COLUMNS:
        service.workflow_definition_key = item["workflow_template"]
    if "required_documents" in SERVICE_COLUMNS:
        service.required_documents = list(item["required_documents"])
    if "visibility" in SERVICE_COLUMNS:
        service.visibility = item["visibility"]
    if "version" in SERVICE_COLUMNS:
        service.version = 1
    if "business_priority" in SERVICE_COLUMNS:
        service.business_priority = int(item["business_priority"])


async def seed_catalog(target_services: int, dry_run: bool) -> dict[str, int]:
    modules_payload = [asdict(item) for item in MODULE_BLUEPRINTS]
    services_payload = [asdict(item) for item in build_service_blueprints(target_services)]

    async with AsyncSessionLocal() as session:
        try:
            existing_modules_result = await session.execute(
                select(Module).where(Module.slug.in_([item["slug"] for item in modules_payload]))
            )
            existing_modules = {item.slug: item for item in existing_modules_result.scalars().all()}
        except ProgrammingError as exc:
            message = str(exc).lower()
            if (
                'relation "modules" does not exist' in message
                or 'relation "services" does not exist' in message
            ):
                raise RuntimeError(
                    "Catalog tables not found. Run database migrations before seeding "
                    "(alembic upgrade head, including 20260228_002_catalog_schema)."
                ) from exc
            raise

        module_created = 0
        module_updated = 0
        for order, item in enumerate(modules_payload, start=1):
            module = existing_modules.get(item["slug"])
            if module:
                module.title = item["title"]
                module.description = item["description"]
                module.icon = item["slug"]
                module.color = "#0B5E8E"
                module.is_active = True
                module.is_foundational = item["is_foundational"]
                module.order = order
                module_updated += 1
            else:
                module = Module(
                    slug=item["slug"],
                    title=item["title"],
                    description=item["description"],
                    icon=item["slug"],
                    color="#0B5E8E",
                    is_active=True,
                    is_foundational=item["is_foundational"],
                    order=order,
                )
                session.add(module)
                existing_modules[item["slug"]] = module
                module_created += 1

        await session.flush()

        service_codes = [item["code"] for item in services_payload]
        existing_services: dict[str, Service] = {}
        for chunked_codes in _chunk(service_codes):
            result = await session.execute(select(Service).where(Service.code.in_(chunked_codes)))
            for service in result.scalars().all():
                existing_services[service.code] = service

        service_created = 0
        service_updated = 0
        for item in services_payload:
            module = existing_modules[item["module_slug"]]
            existing = existing_services.get(item["code"])
            if existing:
                _apply_service_update(existing, item, module.id)
                service_updated += 1
                continue

            service = Service(**_service_create_data(item=item, module_id=module.id))
            session.add(service)
            service_created += 1

        if dry_run:
            await session.rollback()
        else:
            await session.commit()

    return {
        "module_created": module_created,
        "module_updated": module_updated,
        "service_created": service_created,
        "service_updated": service_updated,
        "target_services": target_services,
        "target_modules": len(modules_payload),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed institutional catalog for SILA")
    parser.add_argument(
        "--target-services",
        type=int,
        default=900,
        help="Target number of service records to maintain (default: 900).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate without commit.")
    return parser.parse_args()


async def _main() -> None:
    args = _parse_args()
    try:
        result = await seed_catalog(target_services=args.target_services, dry_run=args.dry_run)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}")
        return
    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"[{mode}] modules={result['target_modules']} services={result['target_services']}")
    print(
        "created: "
        f"modules={result['module_created']} services={result['service_created']} | "
        f"updated: modules={result['module_updated']} services={result['service_updated']}"
    )


if __name__ == "__main__":
    asyncio.run(_main())
