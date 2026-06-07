#!/usr/bin/env python3
"""Scaffold a standardized backend module with clean architecture folders."""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
APP_MODULES_ROOT = BACKEND_ROOT / "app" / "modules"
TESTS_MODULES_ROOT = BACKEND_ROOT / "tests" / "modules"
DOCS_MODULES_ROOT = PROJECT_ROOT / "docs" / "modules"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def slugify(name: str) -> str:
    normalized = name.strip().lower().replace(" ", "-").replace("_", "-")
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    return normalized


def package_name_from_slug(slug: str) -> str:
    # Keep catalog slug for business identity, but use Python-safe package names.
    return slug.replace("-", "_")


def _write_file(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def scaffold_module(name: str, force: bool = False) -> dict[str, int]:
    slug = slugify(name)
    package_name = package_name_from_slug(slug)
    title = " ".join(part.capitalize() for part in slug.split("-"))
    module_root = APP_MODULES_ROOT / package_name
    tests_root = TESTS_MODULES_ROOT / package_name
    doc_file = DOCS_MODULES_ROOT / f"{slug}.md"

    created = 0
    created += int(_write_file(module_root / "__init__.py", "", force))
    created += int(_write_file(module_root / "api" / "__init__.py", "", force))
    created += int(
        _write_file(
            module_root / "api" / "router.py",
            (
                "from fastapi import APIRouter\n\n"
                f'router = APIRouter(prefix="/{slug}", tags=["{title}"])\n'
            ),
            force,
        )
    )
    created += int(_write_file(module_root / "application" / "__init__.py", "", force))
    created += int(
        _write_file(
            module_root / "application" / "service.py",
            (
                f"class {title.replace(' ', '')}Service:\n"
                '    """Application service entrypoint for module use cases."""\n\n'
                "    pass\n"
            ),
            force,
        )
    )
    created += int(_write_file(module_root / "domain" / "__init__.py", "", force))
    created += int(
        _write_file(
            module_root / "domain" / "entities.py",
            "from dataclasses import dataclass\n\n\n"
            "@dataclass\n"
            "class DomainEntity:\n"
            '    """Replace with concrete domain entities."""\n\n'
            "    id: str\n",
            force,
        )
    )
    created += int(_write_file(module_root / "infrastructure" / "__init__.py", "", force))
    created += int(
        _write_file(
            module_root / "infrastructure" / "repository.py",
            'class Repository:\n    """Infrastructure adapter placeholder."""\n\n    pass\n',
            force,
        )
    )
    created += int(
        _write_file(
            module_root / "README.md",
            (
                f"# {title}\n\n"
                "## Architecture\n"
                "- api\n"
                "- application\n"
                "- domain\n"
                "- infrastructure\n\n"
                "## Notes\n"
                "Fill use cases and adapters before exposing endpoints in production.\n"
            ),
            force,
        )
    )
    created += int(
        _write_file(
            tests_root / f"test_{slug.replace('-', '_')}_smoke.py",
            (
                "def test_module_scaffold_importable():\n"
                "    # Smoke check for generated test scaffold.\n"
                "    assert True\n"
            ),
            force,
        )
    )
    created += int(
        _write_file(
            doc_file,
            (
                f"# {title}\n\n"
                "## Scope\n"
                "Describe module objectives and service boundaries.\n\n"
                "## Dependencies\n"
                "- Core identity\n"
                "- Core order engine\n"
                "- Core payments (if billable)\n"
            ),
            force,
        )
    )

    return {"files_created_or_updated": created, "slug": slug, "title": title}


async def register_module_catalog(name: str, order: int | None) -> None:
    from apps.backend.app.core.catalog.models.module import Module
    from apps.backend.app.core.db import AsyncSessionLocal
    from sqlalchemy import select

    slug = slugify(name)
    title = " ".join(part.capitalize() for part in slug.split("-"))

    async with AsyncSessionLocal() as session:
        existing = (
            (await session.execute(select(Module).where(Module.slug == slug))).scalars().first()
        )
        if existing:
            existing.title = title
            existing.description = f"Modulo {title} criado por scaffolder."
            existing.is_active = True
            existing.order = order or existing.order
        else:
            session.add(
                Module(
                    slug=slug,
                    title=title,
                    description=f"Modulo {title} criado por scaffolder.",
                    icon=slug,
                    color="#0B5E8E",
                    is_active=True,
                    is_foundational=False,
                    order=order or 999,
                )
            )
        await session.commit()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create standardized backend module scaffold.")
    parser.add_argument("name", help="Module name or slug.")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite scaffold files if they exist."
    )
    parser.add_argument(
        "--register-db",
        action="store_true",
        help="Also upsert module metadata in catalog table.",
    )
    parser.add_argument(
        "--order", type=int, default=None, help="Catalog order when --register-db is used."
    )
    return parser.parse_args()


async def _main() -> None:
    args = _parse_args()
    result = scaffold_module(name=args.name, force=args.force)
    if args.register_db:
        await register_module_catalog(name=args.name, order=args.order)
    print(
        f"module={result['slug']} files={result['files_created_or_updated']} "
        f"register_db={'yes' if args.register_db else 'no'}"
    )


if __name__ == "__main__":
    asyncio.run(_main())
