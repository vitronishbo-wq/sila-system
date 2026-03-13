import pytest
from unittest.mock import AsyncMock
from app.modules.governance.administracao_local.domain.entities import AdministradorLocal
from app.modules.governance.administracao_local.application.service import AdministracaoLocalService

def test_get_administrador_service():
    async def run_test():
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
    
    import asyncio
    asyncio.run(run_test())
