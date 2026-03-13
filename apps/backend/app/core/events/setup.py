"""Setup scripts for Redis and infrastructure - Phase 19"""
import asyncio
import subprocess
import logging
from pathlib import Path
logger = logging.getLogger('events.setup')

async def setup_redis():
    """Install and start Redis server"""
    try:
        result = subprocess.run(['redis-cli', '--version'], capture_output=True)
        if result.returncode != 0:
            logger.warning('Redis not found. Installing...')
            subprocess.run(['sudo', 'apt', 'install', 'redis-server', '-y'], check=True)
        subprocess.run(['sudo', 'service', 'redis-server', 'start'], check=True)
        logger.info('Redis server started')
    except Exception as e:
        logger.error(f'Redis setup error: {e}')

async def setup_postgres_outbox_table(db_url: str):
    """Create outbox table in PostgreSQL"""
    from sqlalchemy import create_engine
    from app.core.db.base_class import Base
    from app.core.events.outbox.outbox_model import OutboxEvent
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(bind=engine)
        logger.info('Outbox table created')
    except Exception as e:
        logger.error(f'Outbox table creation error: {e}')

async def setup_all(redis_url: str=None, db_url: str=None):
    """Run all setup tasks"""
    await setup_redis()
    if db_url:
        await setup_postgres_outbox_table(db_url)
if __name__ == '__main__':
    import sys
    from app.core.settings import settings
    asyncio.run(setup_all(db_url=settings.DATABASE_URL))