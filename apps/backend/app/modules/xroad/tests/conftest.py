import pytest
import sys
from pathlib import Path
module_root = Path(__file__).parent.parent
sys.path.insert(0, str(module_root))

@pytest.fixture(scope='session')
def event_loop():
    """Event loop for async tests"""
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture
def mock_db():
    """Mock database fixture"""

    class MockDB:

        async def query(self, sql):
            return []

        async def execute(self, sql, params=None):
            return None
    return MockDB()

@pytest.fixture
def mock_repository():
    """Mock repository fixture"""

    class MockRepository:

        async def find_all(self):
            return []

        async def find_by_id(self, id):
            return None

        async def save(self, entity):
            return entity

        async def delete(self, id):
            pass
    return MockRepository()