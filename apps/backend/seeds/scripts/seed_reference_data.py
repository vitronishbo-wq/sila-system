"""
Seed script para dados de referência (localizações, catálogos, etc.)
"""

import asyncio
import logging

logger = logging.getLogger(__name__)


async def run():
    """
    Funciona como placeholder para reference data seeding.
    Atual, as locactions (províncias, municípios) são seeded em seed_base_users.py
    """
    logger.info("✓ Reference data seeding completed")
    return True


if __name__ == "__main__":
    asyncio.run(run())
