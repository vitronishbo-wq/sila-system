import asyncio
from unittest.mock import AsyncMock
import sys
import os

# Set PYTHONPATH
sys.path.append(os.path.join(os.getcwd(), "apps", "backend"))

from apps.backend.app.modules.administracao_local.domain.entities import AdministradorLocal
from apps.backend.app.modules.administracao_local.application.service import AdministracaoLocalService

async def test_get_administrador_service():
    print("Running functional test...")
    # 1. Instantiate a domain entity
    expected_admin = AdministradorLocal(id="123", nome="João Silva", cargo="Gerente")
    
    # 2. Mock the repository
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = expected_admin
    
    # 3. Call the application service
    service = AdministracaoLocalService(repository=mock_repo)
    result = await service.get_administrador("123")
    
    # 4. Validate expected behavior
    assert result.id == "123"
    assert result.nome == "João Silva"
    mock_repo.get_by_id.assert_called_once_with("123")
    print("Test passed! ✔")

if __name__ == "__main__":
    asyncio.run(test_get_administrador_service())
