import asyncio
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def app_root():
    """Application root path"""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def mock_logger():
    """Mock logger fixture"""

    class MockLogger:
        def info(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            pass

        def debug(self, msg):
            pass

    return MockLogger()
