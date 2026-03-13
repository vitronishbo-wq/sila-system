#!/usr/bin/env python3
"""Bulk-create module scaffolds for all institutional blueprint modules."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = PROJECT_ROOT / "apps" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.catalog.blueprint import MODULE_BLUEPRINTS
from create_module import register_module_catalog, scaffold_module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap all institutional modules.")
    parser.add_argument("--force", action="store_true", help="Overwrite scaffold files when they already exist.")
    parser.add_argument(
        "--register-db",
        action="store_true",
        help="Upsert module metadata into catalog table while scaffolding.",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    created_files = 0
    for order, module in enumerate(MODULE_BLUEPRINTS, start=1):
        result = scaffold_module(module.slug, force=args.force)
        created_files += int(result["files_created_or_updated"])
        if args.register_db:
            await register_module_catalog(module.slug, order=order)
        print(
            f"module={module.slug} files={result['files_created_or_updated']} "
            f"register_db={'yes' if args.register_db else 'no'}"
        )

    print(
        f"done modules={len(MODULE_BLUEPRINTS)} total_files_created_or_updated={created_files} "
        f"register_db={'yes' if args.register_db else 'no'}"
    )


if __name__ == "__main__":
    asyncio.run(main())
