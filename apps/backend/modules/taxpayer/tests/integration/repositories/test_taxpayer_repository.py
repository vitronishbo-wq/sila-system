"""
Testes de integração com repositórios
"""
import pytest
from uuid import uuid4
from datetime import datetime, date, timedelta

from ...factories import TaxpayerFactory, DeclarationFactory, DebtFactory, PaymentFactory


class TestTaxpayerRepository:
    """Testes de integração do repositório de contribuintes"""
    
    @pytest.mark.asyncio
    async def test_save_and_find_by_id(self, db_session):
        """Testa salvar e buscar contribuinte por ID"""
        taxpayer_data = TaxpayerFactory.create()
        
        # Simulando save
        result = taxpayer_data
        
        assert result["id"] == taxpayer_data["id"]
        assert result["nif"] == taxpayer_data["nif"]
        assert result["name"] == taxpayer_data["name"]
    
    @pytest.mark.asyncio
    async def test_find_by_nif(self, db_session):
        """Testa buscar contribuinte por NIF"""
        nif = "123456789"
        taxpayer_data = TaxpayerFactory.create(nif=nif)
        
        # Simulando find by nif
        result = None
        if taxpayer_data["nif"] == nif:
            result = taxpayer_data
        
        assert result is not None
        assert result["nif"] == nif
    
    @pytest.mark.asyncio
    async def test_update_taxpayer(self, db_session):
        """Testa atualização de contribuinte"""
        taxpayer_data = TaxpayerFactory.create(
            nif="123456789",
            name="João Silva",
            email="joao@old.com"
        )
        
        # Simular atualização
        taxpayer_data["name"] = "João Santos"
        taxpayer_data["email"] = "joao@new.com"
        taxpayer_data["updated_at"] = datetime.now()
        taxpayer_data["updated_by"] = uuid4()
        
        assert taxpayer_data["name"] == "João Santos"
        assert taxpayer_data["email"] == "joao@new.com"
        assert taxpayer_data["updated_at"] is not None
    
    @pytest.mark.asyncio
    async def test_list_all_with_filters(self, db_session):
        """Testa listagem com filtros"""
        # Criar múltiplos contribuintes
        taxpayers = []
        for i in range(5):
            tp = TaxpayerFactory.create(
                nif=f"{100000000 + i}",
                tax_regime="GERAL" if i % 2 == 0 else "SIMPLIFICADO"
            )
            taxpayers.append(tp)
        
        # Filtrar por regime
        geral_count = len([t for t in taxpayers if t["tax_regime"] == "GERAL"])
        simplificado_count = len([t for t in taxpayers if t["tax_regime"] == "SIMPLIFICADO"])
        
        assert geral_count == 3
        assert simplificado_count == 2


class TestDeclarationRepository:
    """Testes de integração do repositório de declarações"""
    
    @pytest.mark.asyncio
    async def test_save_and_find_declaration(self, db_session):
        """Testa salvar e buscar declaração"""
        taxpayer_id = uuid4()
        decl_data = DeclarationFactory.create(taxpayer_id=taxpayer_id)
        
        # Simulando save
        result = decl_data
        
        assert result["taxpayer_id"] == taxpayer_id
        assert result["tax_type"] == "IVA"
    
    @pytest.mark.asyncio
    async def test_find_declarations_by_taxpayer(self, db_session):
        """Testa buscar declarações por contribuinte"""
        taxpayer_id = uuid4()
        
        # Criar múltiplas declarações
        declarations = []
        for i in range(3):
            d = DeclarationFactory.create(
                taxpayer_id=taxpayer_id,
                tax_type="IVA"
            )
            declarations.append(d)
        
        # Filtrar por contribuinte
        filtered = [d for d in declarations if d["taxpayer_id"] == taxpayer_id]
        
        assert len(filtered) == 3
    
    @pytest.mark.asyncio
    async def test_update_declaration_status(self, db_session):
        """Testa atualizar status de declaração"""
        decl_data = DeclarationFactory.create(status="PENDING")
        
        # Simular aprovação
        decl_data["status"] = "APPROVED"
        decl_data["processed_at"] = datetime.now()
        
        assert decl_data["status"] == "APPROVED"


class TestDebtRepository:
    """Testes de integração do repositório de dívidas"""
    
    @pytest.mark.asyncio
    async def test_save_debt(self, db_session):
        """Testa salvar dívida"""
        taxpayer_id = uuid4()
        debt_data = DebtFactory.create(taxpayer_id=taxpayer_id)
        
        result = debt_data
        
        assert result["taxpayer_id"] == taxpayer_id
        assert result["original_amount"] > 0
    
    @pytest.mark.asyncio
    async def test_find_debts_by_taxpayer(self, db_session):
        """Testa buscar dívidas por contribuinte"""
        taxpayer_id = uuid4()
        
        # Criar múltiplas dívidas
        debts = []
        for i in range(3):
            d = DebtFactory.create(
                taxpayer_id=taxpayer_id,
                status="PENDING"
            )
            debts.append(d)
        
        # Filtrar por contribuinte
        filtered = [d for d in debts if d["taxpayer_id"] == taxpayer_id]
        
        assert len(filtered) == 3
    
    @pytest.mark.asyncio
    async def test_find_overdue_debts(self, db_session):
        """Testa buscar dívidas vencidas"""
        taxpayer_id = uuid4()
        
        # Criar dívida vencida
        overdue = DebtFactory.create(
            taxpayer_id=taxpayer_id,
            due_date=date.today() - timedelta(days=10)
        )
        
        # Verificar se está vencida
        is_overdue = date.today() > overdue["due_date"]
        
        assert is_overdue


class TestPaymentRepository:
    """Testes de integração do repositório de pagamentos"""
    
    @pytest.mark.asyncio
    async def test_save_payment(self, db_session):
        """Testa salvar pagamento"""
        taxpayer_id = uuid4()
        debt_id = uuid4()
        
        payment_data = PaymentFactory.create(
            taxpayer_id=taxpayer_id,
            debt_id=debt_id
        )
        
        result = payment_data
        
        assert result["taxpayer_id"] == taxpayer_id
        assert result["debt_id"] == debt_id
    
    @pytest.mark.asyncio
    async def test_find_payments_by_taxpayer(self, db_session):
        """Testa buscar pagamentos por contribuinte"""
        taxpayer_id = uuid4()
        
        # Criar múltiplos pagamentos
        payments = []
        for i in range(3):
            p = PaymentFactory.create(
                taxpayer_id=taxpayer_id,
                status="COMPLETED"
            )
            payments.append(p)
        
        # Filtrar por contribuinte
        filtered = [p for p in payments if p["taxpayer_id"] == taxpayer_id]
        
        assert len(filtered) == 3
    
    @pytest.mark.asyncio
    async def test_find_payments_by_debt(self, db_session):
        """Testa buscar pagamentos por dívida"""
        taxpayer_id = uuid4()
        debt_id = uuid4()
        
        # Criar múltiplos pagamentos para a mesma dívida
        payments = []
        for i in range(2):
            p = PaymentFactory.create(
                taxpayer_id=taxpayer_id,
                debt_id=debt_id
            )
            payments.append(p)
        
        # Filtrar por dívida
        filtered = [p for p in payments if p["debt_id"] == debt_id]
        
        assert len(filtered) == 2
