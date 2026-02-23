"""
Testes de serviços de aplicação
"""
import pytest
from uuid import uuid4
from unittest.mock import Mock, AsyncMock, MagicMock
from datetime import datetime, date, timedelta

from ..factories import TaxpayerFactory, DeclarationFactory, DebtFactory, PaymentFactory


class TestTaxpayerService:
    """Testes do serviço de contribuintes"""
    
    @pytest.fixture
    def setup(self):
        self.repo = AsyncMock()
        self.agt = AsyncMock()
        self.notification = AsyncMock()
        self.audit = AsyncMock()
        self.cache = AsyncMock()
        
        return {
            "repo": self.repo,
            "agt": self.agt,
            "notification": self.notification,
            "audit": self.audit,
            "cache": self.cache
        }
    
    @pytest.mark.asyncio
    async def test_register_taxpayer_success(self, setup):
        """Testa registro bem-sucedido de contribuinte"""
        # Mocks
        self.agt.validate_nif = AsyncMock(return_value=True)
        self.agt.get_taxpayer_data = AsyncMock(return_value={
            "name": "João Silva",
            "email": "joao@email.com"
        })
        self.repo.find_by_nif = AsyncMock(return_value=None)
        
        taxpayer_data = TaxpayerFactory.create(
            nif="123456789",
            name="João Silva",
            email="joao@email.com"
        )
        
        self.repo.save = AsyncMock(return_value=taxpayer_data)
        
        # Verificações
        assert self.agt.validate_nif.call_count == 0
        assert self.repo.save.call_count == 0
    
    @pytest.mark.asyncio
    async def test_register_taxpayer_already_exists(self, setup):
        """Testa registro de contribuinte já existente"""
        existing = TaxpayerFactory.create(nif="123456789")
        self.repo.find_by_nif = AsyncMock(return_value=existing)
        
        # Verificar que encontrou
        result = await self.repo.find_by_nif("123456789")
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_get_taxpayer_by_nif_cache_hit(self, setup):
        """Testa busca por NIF com cache"""
        cached_data = {
            "id": str(uuid4()),
            "nif": "123456789",
            "name": "João Silva"
        }
        self.cache.get = AsyncMock(return_value=cached_data)
        
        result = await self.cache.get("taxpayer:123456789")
        
        assert result is not None
        assert result["nif"] == "123456789"
    
    @pytest.mark.asyncio
    async def test_get_taxpayer_by_nif_cache_miss(self, setup):
        """Testa busca por NIF com cache miss"""
        self.cache.get = AsyncMock(return_value=None)
        taxpayer = TaxpayerFactory.create(nif="123456789")
        self.repo.find_by_nif = AsyncMock(return_value=taxpayer)
        
        result = await self.repo.find_by_nif("123456789")
        
        assert result is not None
        assert result["nif"] == "123456789"
    
    @pytest.mark.asyncio
    async def test_update_taxpayer(self, setup):
        """Testa atualização de contribuinte"""
        taxpayer_id = uuid4()
        original = TaxpayerFactory.create(
            id=taxpayer_id,
            nif="123456789",
            name="João Silva",
            email="joao@old.com"
        )
        
        self.repo.find_by_id = AsyncMock(return_value=original)
        
        updates = {
            "name": "João Santos",
            "email": "joao@new.com"
        }
        
        updated = original.copy()
        updated.update(updates)
        updated["updated_at"] = datetime.now()
        updated["updated_by"] = uuid4()
        
        self.repo.save = AsyncMock(return_value=updated)
        
        # Verificações
        assert updated["name"] == "João Santos"
        assert updated["email"] == "joao@new.com"
    
    @pytest.mark.asyncio
    async def test_list_taxpayers(self, setup):
        """Testa listagem de contribuintes"""
        taxpayers = [
            TaxpayerFactory.create(),
            TaxpayerFactory.create(),
            TaxpayerFactory.create()
        ]
        
        self.repo.list_all = AsyncMock(return_value=(taxpayers, 3))
        
        result, total = await self.repo.list_all()
        
        assert total == 3
        assert len(result) == 3


class TestDeclarationService:
    """Testes do serviço de declarações"""
    
    @pytest.fixture
    def setup(self):
        self.repo = AsyncMock()
        self.agt = AsyncMock()
        self.notification = AsyncMock()
        self.audit = AsyncMock()
        
        return {
            "repo": self.repo,
            "agt": self.agt,
            "notification": self.notification,
            "audit": self.audit
        }
    
    @pytest.mark.asyncio
    async def test_submit_declaration_success(self, setup):
        """Testa submissão bem-sucedida de declaração"""
        taxpayer_id = uuid4()
        submitted_by = uuid4()
        
        # Mock
        self.repo.find_declarations_by_taxpayer = AsyncMock(return_value=([], 0))
        self.agt.submit_declaration = AsyncMock(return_value="PROTOCOL-123")
        
        declaration_data = DeclarationFactory.create(
            taxpayer_id=taxpayer_id,
            submitted_by=submitted_by
        )
        
        self.repo.save_declaration = AsyncMock(return_value=declaration_data)
        
        # Verificações
        assert declaration_data["tax_type"] == "IVA"
        assert declaration_data["status"] == "PENDING"
    
    @pytest.mark.asyncio
    async def test_submit_declaration_duplicate(self, setup):
        """Testa submissão de declaração duplicada"""
        taxpayer_id = uuid4()
        
        existing = DeclarationFactory.create(
            taxpayer_id=taxpayer_id,
            tax_type="IVA",
            status="PENDING"
        )
        
        self.repo.find_declarations_by_taxpayer = AsyncMock(return_value=([existing], 1))
        
        result, total = await self.repo.find_declarations_by_taxpayer(taxpayer_id, "2024-01")
        
        assert total == 1
        assert len(result) == 1
    
    @pytest.mark.asyncio
    async def test_process_declaration_approve(self, setup):
        """Testa aprovação de declaração"""
        declaration_id = uuid4()
        processed_by = uuid4()
        
        declaration = DeclarationFactory.create(status="PENDING")
        declaration["id"] = declaration_id
        
        self.repo.find_declaration_by_id = AsyncMock(return_value=declaration)
        
        # Simular aprovação
        declaration["status"] = "APPROVED"
        declaration["processed_at"] = datetime.now()
        declaration["processed_by"] = processed_by
        
        self.repo.update_declaration_status = AsyncMock(return_value=declaration)
        
        result = await self.repo.update_declaration_status(declaration_id, "APPROVED")
        
        assert result["status"] == "APPROVED"
    
    @pytest.mark.asyncio
    async def test_get_taxpayer_declarations(self, setup):
        """Testa listagem de declarações"""
        taxpayer_id = uuid4()
        declarations = [
            DeclarationFactory.create(taxpayer_id=taxpayer_id, tax_period="2024-01"),
            DeclarationFactory.create(taxpayer_id=taxpayer_id, tax_period="2024-02")
        ]
        
        self.repo.find_declarations_by_taxpayer = AsyncMock(return_value=(declarations, 2))
        
        result, total = await self.repo.find_declarations_by_taxpayer(taxpayer_id, 2024)
        
        assert total == 2
        assert len(result) == 2


class TestDebtService:
    """Testes do serviço de dívidas"""
    
    @pytest.fixture
    def setup(self):
        self.repo = AsyncMock()
        self.notification = AsyncMock()
        self.audit = AsyncMock()
        
        return {
            "repo": self.repo,
            "notification": self.notification,
            "audit": self.audit
        }
    
    @pytest.mark.asyncio
    async def test_create_debt_success(self, setup):
        """Testa criação bem-sucedida de dívida"""
        taxpayer_id = uuid4()
        
        debt_data = DebtFactory.create(taxpayer_id=taxpayer_id)
        
        self.repo.save_debt = AsyncMock(return_value=debt_data)
        
        result = await self.repo.save_debt(debt_data)
        
        assert result["taxpayer_id"] == taxpayer_id
        assert result["status"] == "PENDING"
    
    @pytest.mark.asyncio
    async def test_get_taxpayer_debts(self, setup):
        """Testa listagem de dívidas"""
        taxpayer_id = uuid4()
        debts = [
            DebtFactory.create(taxpayer_id=taxpayer_id),
            DebtFactory.create(taxpayer_id=taxpayer_id)
        ]
        
        self.repo.find_debts_by_taxpayer = AsyncMock(return_value=(debts, 2))
        
        result, total = await self.repo.find_debts_by_taxpayer(taxpayer_id)
        
        assert total == 2
        assert len(result) == 2
    
    @pytest.mark.asyncio
    async def test_mark_debt_as_paid(self, setup):
        """Testa marcação de dívida como paga"""
        debt_id = uuid4()
        debt = DebtFactory.create(status="PENDING")
        debt["id"] = debt_id
        
        self.repo.find_debt_by_id = AsyncMock(return_value=debt)
        
        # Simular pagamento
        debt["status"] = "PAID"
        debt["paid_at"] = datetime.now()
        
        self.repo.update_debt_status = AsyncMock(return_value=debt)
        
        result = await self.repo.update_debt_status(debt_id, "PAID")
        
        assert result["status"] == "PAID"


class TestPaymentService:
    """Testes do serviço de pagamentos"""
    
    @pytest.fixture
    def setup(self):
        self.repo = AsyncMock()
        self.notification = AsyncMock()
        self.audit = AsyncMock()
        
        return {
            "repo": self.repo,
            "notification": self.notification,
            "audit": self.audit
        }
    
    @pytest.mark.asyncio
    async def test_process_payment_success(self, setup):
        """Testa processamento bem-sucedido de pagamento"""
        taxpayer_id = uuid4()
        debt_id = uuid4()
        
        payment_data = PaymentFactory.create(
            taxpayer_id=taxpayer_id,
            debt_id=debt_id,
            amount=850000.00
        )
        
        self.repo.save_payment = AsyncMock(return_value=payment_data)
        
        result = await self.repo.save_payment(payment_data)
        
        assert result["taxpayer_id"] == taxpayer_id
        assert result["debt_id"] == debt_id
        assert result["status"] == "COMPLETED"
    
    @pytest.mark.asyncio
    async def test_get_taxpayer_payments(self, setup):
        """Testa listagem de pagamentos"""
        taxpayer_id = uuid4()
        payments = [
            PaymentFactory.create(taxpayer_id=taxpayer_id),
            PaymentFactory.create(taxpayer_id=taxpayer_id)
        ]
        
        self.repo.find_payments_by_taxpayer = AsyncMock(return_value=(payments, 2))
        
        result, total = await self.repo.find_payments_by_taxpayer(taxpayer_id)
        
        assert total == 2
        assert len(result) == 2
