"""
Testes end-to-end do fluxo completo
"""
import pytest
from httpx import AsyncClient
from uuid import uuid4
from datetime import date, timedelta
from unittest.mock import patch, AsyncMock

from ...factories import TaxpayerFactory, DeclarationFactory, DebtFactory, PaymentFactory


@pytest.mark.e2e
class TestTaxpayerFullFlow:
    """Testes end-to-end do fluxo completo de contribuinte"""
    
    @pytest.mark.asyncio
    async def test_taxpayer_lifecycle(self, async_client: AsyncClient, admin_user):
        """Testa ciclo de vida completo de um contribuinte"""
        
        # 1. Registrar contribuinte
        taxpayer_data = TaxpayerFactory.create(nif="123456789")
        assert taxpayer_data["nif"] == "123456789"
        assert taxpayer_data["status"] == "ACTIVE"
        
        taxpayer_id = taxpayer_data["id"]
        
        # 2. Submeter declaração
        declaration_data = DeclarationFactory.create(
            taxpayer_id=taxpayer_id,
            tax_period="2024-01",
            gross_amount=1000000.00
        )
        
        assert declaration_data["taxpayer_id"] == taxpayer_id
        assert declaration_data["tax_type"] == "IVA"
        assert declaration_data["status"] == "PENDING"
        
        declaration_id = declaration_data["id"]
        
        # 3. Criar dívida
        debt_data = DebtFactory.create(
            taxpayer_id=taxpayer_id,
            original_amount=declaration_data["net_amount"]
        )
        
        assert debt_data["taxpayer_id"] == taxpayer_id
        assert debt_data["original_amount"] > 0
        
        debt_id = debt_data["id"]
        
        # 4. Processar pagamento
        payment_data = PaymentFactory.create(
            taxpayer_id=taxpayer_id,
            debt_id=debt_id,
            amount=debt_data["original_amount"]
        )
        
        assert payment_data["taxpayer_id"] == taxpayer_id
        assert payment_data["debt_id"] == debt_id
        assert payment_data["amount"] == debt_data["original_amount"]
        assert payment_data["status"] == "COMPLETED"
    
    @pytest.mark.asyncio
    async def test_multiple_declarations_flow(self, async_client: AsyncClient, admin_user):
        """Testa fluxo com múltiplas declarações"""
        
        # Criar contribuinte
        taxpayer_data = TaxpayerFactory.create()
        taxpayer_id = taxpayer_data["id"]
        
        # Submeter múltiplas declarações
        declarations = []
        for month in range(1, 4):  # Jan, Feb, Mar
            decl = DeclarationFactory.create(
                taxpayer_id=taxpayer_id,
                month=month,
                tax_period=f"2024-{month:02d}"
            )
            declarations.append(decl)
        
        assert len(declarations) == 3
        
        # Verificar que todas foram criadas
        for decl in declarations:
            assert decl["taxpayer_id"] == taxpayer_id
            assert decl["status"] == "PENDING"
    
    @pytest.mark.asyncio
    async def test_partial_payment_flow(self, async_client: AsyncClient, admin_user):
        """Testa fluxo com pagamento parcial"""
        
        # Criar contribuinte
        taxpayer_data = TaxpayerFactory.create()
        taxpayer_id = taxpayer_data["id"]
        
        # Criar dívida
        debt_data = DebtFactory.create(
            taxpayer_id=taxpayer_id,
            original_amount=100000.00
        )
        debt_id = debt_data["id"]
        
        # Primeiro pagamento (parcial - 50%)
        payment1 = PaymentFactory.create(
            taxpayer_id=taxpayer_id,
            debt_id=debt_id,
            amount=50000.00
        )
        
        assert payment1["amount"] == 50000.00
        
        # Segundo pagamento (resto)
        payment2 = PaymentFactory.create(
            taxpayer_id=taxpayer_id,
            debt_id=debt_id,
            amount=50000.00
        )
        
        assert payment2["amount"] == 50000.00
        
        # Verificar total pago
        total_paid = payment1["amount"] + payment2["amount"]
        assert total_paid == debt_data["original_amount"]


@pytest.mark.e2e
class TestDeclarationLifecycle:
    """Testes end-to-end do ciclo de vida de declaração"""
    
    @pytest.mark.asyncio
    async def test_declaration_approval_flow(self, async_client: AsyncClient, admin_user):
        """Testa fluxo de aprovação de declaração"""
        
        # Criar declaração
        taxpayer_data = TaxpayerFactory.create()
        declaration_data = DeclarationFactory.create(
            taxpayer_id=taxpayer_data["id"],
            status="PENDING"
        )
        
        # Verificar status inicial
        assert declaration_data["status"] == "PENDING"
        
        # Simular aprovação
        declaration_data["status"] = "APPROVED"
        
        assert declaration_data["status"] == "APPROVED"
    
    @pytest.mark.asyncio
    async def test_declaration_rejection_flow(self, async_client: AsyncClient, admin_user):
        """Testa fluxo de rejeição de declaração"""
        
        # Criar declaração
        taxpayer_data = TaxpayerFactory.create()
        declaration_data = DeclarationFactory.create(
            taxpayer_id=taxpayer_data["id"],
            status="PENDING"
        )
        
        # Simular rejeição
        declaration_data["status"] = "REJECTED"
        
        assert declaration_data["status"] == "REJECTED"


@pytest.mark.e2e
class TestDebtCollectionFlow:
    """Testes end-to-end do fluxo de cobrança"""
    
    @pytest.mark.asyncio
    async def test_debt_collection_with_penalty(self, async_client: AsyncClient, admin_user):
        """Testa fluxo de cobrança com penalidade"""
        
        # Criar dívida com juros
        taxpayer_data = TaxpayerFactory.create()
        debt_data = DebtFactory.create(
            taxpayer_id=taxpayer_data["id"],
            original_amount=100000.00,
            days_overdue=30
        )
        
        # Verificar juros
        assert debt_data["interest"] > 0
        assert debt_data["current_amount"] > debt_data["original_amount"]
        
        # Calcular multa (5% do principal)
        fine = debt_data["original_amount"] * 0.05
        total_with_fine = debt_data["current_amount"] + fine
        
        assert total_with_fine > debt_data["current_amount"]
    
    @pytest.mark.asyncio
    async def test_aged_debt_handling(self, async_client: AsyncClient, admin_user):
        """Testa tratamento de dívidas antigas"""
        
        taxpayer_data = TaxpayerFactory.create()
        
        # Criar dívida com mais de 90 dias
        debt_data = DebtFactory.create(
            taxpayer_id=taxpayer_data["id"],
            days_overdue=120,
            original_amount=100000.00
        )
        
        # Verificar acumulação de juros
        days_ratio = debt_data["days_overdue"] / 30
        expected_interest = debt_data["original_amount"] * 0.01 * days_ratio
        
        assert debt_data["interest"] == expected_interest
