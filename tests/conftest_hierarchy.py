"""
conftest.py para testes de HierarchyService

Configurações e fixtures específicas para os testes de endpoints
"""

import pytest
import asyncio

# Configurar pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="session")
def event_loop():
    """Event loop para testes async"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
