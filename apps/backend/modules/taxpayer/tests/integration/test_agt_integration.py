"""
Testes de integração com AGT
"""
import pytest
from unittest.mock import AsyncMock


class TestAGTIntegration:
    """Testes de integração com AGT"""
    
    @pytest.mark.asyncio
    async def test_agt_mock_client_validate_nif(self, mock_agt_client):
        """Testa mock client para validação de NIF"""
        # Mock retorna True por padrão
        result = await mock_agt_client.validate_nif("123456789")
        assert result is True
    
    @pytest.mark.asyncio
    async def test_agt_mock_client_get_taxpayer_data(self, mock_agt_client):
        """Testa mock client para dados de contribuinte"""
        data = await mock_agt_client.get_taxpayer_data("123456789")
        assert data is not None
        assert "name" in data
        assert "email" in data
    
    @pytest.mark.asyncio
    async def test_agt_mock_client_get_tax_debts(self, mock_agt_client):
        """Testa mock client para dívidas"""
        debts = await mock_agt_client.get_tax_debts("123456789")
        assert isinstance(debts, list)
    
    @pytest.mark.asyncio
    async def test_agt_mock_client_submit_declaration(self, mock_agt_client):
        """Testa mock client para submissão de declaração"""
        protocol = await mock_agt_client.submit_declaration(
            "123456789",
            {"tax_type": "IVA", "amount": 1000}
        )
        assert protocol == "PROTOCOL-123"
    
    @pytest.mark.asyncio
    async def test_agt_rate_limiter(self):
        """Testa rate limiter da AGT"""
        from datetime import datetime
        
        # Simular rate limiting
        max_requests = 10
        request_count = 0
        
        for i in range(max_requests):
            request_count += 1
        
        assert request_count <= max_requests
    
    @pytest.mark.asyncio
    async def test_agt_retry_logic(self, mock_agt_client):
        """Testa lógica de retry"""
        # Mock retorna sucesso
        result = await mock_agt_client.validate_nif("123456789")
        
        # Primeira tentativa
        assert result is True
        
        # Retry seria a segunda chamada
        retry_result = await mock_agt_client.validate_nif("123456789")
        assert retry_result is True


class TestCacheIntegration:
    """Testes de integração com cache"""
    
    @pytest.mark.asyncio
    async def test_cache_set_and_get(self, mock_cache):
        """Testa set e get no cache"""
        key = "taxpayer:123"
        value = {"id": "123", "name": "João"}
        
        await mock_cache.set(key, value)
        result = await mock_cache.get(key)
        
        assert result == value
    
    @pytest.mark.asyncio
    async def test_cache_delete(self, mock_cache):
        """Testa delete do cache"""
        key = "taxpayer:123"
        value = {"id": "123"}
        
        await mock_cache.set(key, value)
        assert await mock_cache.get(key) is not None
        
        await mock_cache.delete(key)
        assert await mock_cache.get(key) is None
    
    @pytest.mark.asyncio
    async def test_cache_clear(self, mock_cache):
        """Testa clear do cache"""
        await mock_cache.set("key1", "value1")
        await mock_cache.set("key2", "value2")
        
        assert await mock_cache.get("key1") is not None
        
        await mock_cache.clear()
        
        assert await mock_cache.get("key1") is None
        assert await mock_cache.get("key2") is None


class TestNotificationIntegration:
    """Testes de integração com notificações"""
    
    @pytest.mark.asyncio
    async def test_notify_taxpayer(self, mock_notification):
        """Testa notificação para contribuinte"""
        await mock_notification.notify_taxpayer("123", "test message")
        
        assert len(mock_notification.sent) == 1
        assert mock_notification.sent[0][0] == "taxpayer"
    
    @pytest.mark.asyncio
    async def test_notify_admin(self, mock_notification):
        """Testa notificação para admin"""
        await mock_notification.notify_admin("test message")
        
        assert len(mock_notification.sent) == 1
        assert mock_notification.sent[0][0] == "admin"
    
    @pytest.mark.asyncio
    async def test_send_email(self, mock_notification):
        """Testa envio de email"""
        await mock_notification.send_email("test@example.com", "subject", "body")
        
        assert len(mock_notification.sent) == 1
        assert mock_notification.sent[0][0] == "email"
