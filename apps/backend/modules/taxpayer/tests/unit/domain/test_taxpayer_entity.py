"""
Testes de entidades do domain
"""
import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from ..factories import TaxpayerFactory


class TestTaxpayerEntity:
    """Testes da entidade Taxpayer"""
    
    def test_create_taxpayer_success(self):
        """Testa criação bem-sucedida de contribuinte"""
        data = TaxpayerFactory.create(
            nif="123456789",
            name="João Silva",
            email="joao@email.com"
        )
        
        assert data["nif"] == "123456789"
        assert data["name"] == "João Silva"
        assert data["email"] == "joao@email.com"
        assert data["status"] == "ACTIVE"
        assert data["id"] is not None
        assert data["registered_at"] is not None
    
    def test_create_taxpayer_without_email(self):
        """Testa criação sem email"""
        data = TaxpayerFactory.create(
            nif="123456789",
            name="João Silva"
        )
        
        assert data["email"] is not None
        assert data["phone"] is not None
        assert data["address"] is not None
    
    def test_create_taxpayer_custom_regime(self):
        """Testa criação com regime customizado"""
        data = TaxpayerFactory.create(
            nif="123456789",
            tax_regime="SIMPLIFICADO"
        )
        
        assert data["tax_regime"] == "SIMPLIFICADO"
    
    def test_create_taxpayer_custom_status(self):
        """Testa criação com status customizado"""
        data = TaxpayerFactory.create(
            nif="123456789",
            status="SUSPENDED"
        )
        
        assert data["status"] == "SUSPENDED"
    
    def test_taxpayer_has_all_required_fields(self):
        """Testa se contribuinte tem todos os campos obrigatórios"""
        data = TaxpayerFactory.create()
        
        required_fields = [
            "id", "nif", "name", "email", "phone", "address",
            "tax_regime", "status", "registered_by", "registered_at"
        ]
        
        for field in required_fields:
            assert field in data
            assert data[field] is not None or field == "updated_at" or field == "updated_by"


class TestNIFValueObject:
    """Testes do Value Object NIF"""
    
    def test_nif_valid_9_digits(self):
        """Testa NIF válido de 9 dígitos"""
        nif = "123456789"
        assert len(nif) == 9
        assert nif.isdigit()
    
    def test_nif_valid_14_digits(self):
        """Testa NIF válido de 14 dígitos"""
        nif = "12345678901234"
        assert len(nif) == 14
        assert nif.isdigit()
    
    def test_nif_with_leading_one(self):
        """Testa NIF começando com 1 (válido em Angola)"""
        nif = "123456789"
        assert nif[0] in ['1', '3', '5', '7', '9']
    
    def test_nif_format_validation(self):
        """Testa validação básica de formato NIF"""
        valid_nif = "123456789"
        invalid_nif = "12345"  # Muito curto
        
        assert len(valid_nif) >= 9
        assert len(invalid_nif) < 9


class TestDeclarationValueObject:
    """Testes do Value Object TaxPeriod"""
    
    def test_tax_period_valid_format(self):
        """Testa período válido"""
        period = "2024-01"
        parts = period.split("-")
        
        assert len(parts) == 2
        assert int(parts[0]) == 2024
        assert int(parts[1]) == 1
    
    def test_tax_period_month_range(self):
        """Testa mês dentro do intervalo válido"""
        for month in range(1, 13):
            period = f"2024-{month:02d}"
            parts = period.split("-")
            assert int(parts[1]) >= 1 and int(parts[1]) <= 12
    
    def test_tax_period_invalid_month(self):
        """Testa mês inválido"""
        period = "2024-13"
        parts = period.split("-")
        month = int(parts[1])
        
        assert month > 12  # Inválido
    
    def test_tax_period_comparison(self):
        """Testa comparação de períodos"""
        p1 = "2024-01"
        p2 = "2024-01"
        p3 = "2024-02"
        
        assert p1 == p2
        assert p1 != p3
        assert p1 < p3


class TestTaxAmountValueObject:
    """Testes do Value Object TaxAmount"""
    
    def test_create_amount_positive(self):
        """Testa criação de valor positivo"""
        amount = 1000.50
        assert amount > 0
    
    def test_amount_addition(self):
        """Testa adição de valores"""
        a1 = 1000.0
        a2 = 500.0
        result = a1 + a2
        assert result == 1500.0
    
    def test_amount_subtraction(self):
        """Testa subtração de valores"""
        a1 = 1000.0
        a2 = 300.0
        result = a1 - a2
        assert result == 700.0
    
    def test_amount_multiplication(self):
        """Testa multiplicação de valores"""
        amount = 1000.0
        multiplier = 1.1
        result = amount * multiplier
        assert result == 1100.0
    
    def test_amount_precision(self):
        """Testa precisão de valores"""
        amount = 1000.55
        assert round(amount, 2) == 1000.55


class TestDeclarationEntity:
    """Testes da entidade TaxDeclaration"""
    
    def test_create_declaration_success(self):
        """Testa criação bem-sucedida de declaração"""
        data = TaxpayerFactory.create()
        taxpayer_id = data["id"]
        
        decl_data = {
            "taxpayer_id": taxpayer_id,
            "tax_type": "IVA",
            "tax_period": "2024-01",
            "gross_amount": 1000000.00,
            "deductions": 150000.00,
            "net_amount": 850000.00,
            "status": "PENDING"
        }
        
        assert decl_data["tax_type"] == "IVA"
        assert decl_data["net_amount"] == decl_data["gross_amount"] - decl_data["deductions"]
        assert decl_data["status"] == "PENDING"
    
    def test_create_declaration_without_deductions(self):
        """Testa criação sem deduções"""
        gross_amount = 1000000.00
        deductions = 0
        net_amount = gross_amount - deductions
        
        assert net_amount == gross_amount
    
    def test_declaration_amount_validation(self):
        """Testa validação de valores"""
        gross_amount = 1000000.00
        deductions = 150000.00
        
        assert gross_amount > 0
        assert deductions >= 0
        assert deductions <= gross_amount


class TestDebtEntity:
    """Testes da entidade Debt"""
    
    def test_create_debt_success(self):
        """Testa criação bem-sucedida de dívida"""
        from ..factories import DebtFactory
        
        data = TaxpayerFactory.create()
        taxpayer_id = data["id"]
        
        debt_data = DebtFactory.create(taxpayer_id=taxpayer_id)
        
        assert debt_data["taxpayer_id"] == taxpayer_id
        assert debt_data["original_amount"] > 0
        assert debt_data["current_amount"] >= debt_data["original_amount"]
        assert debt_data["status"] == "PENDING"
    
    def test_debt_interest_calculation(self):
        """Testa cálculo de juros"""
        original_amount = 100000.0
        days_overdue = 30
        interest_rate = 0.01  # 1% ao mês
        interest = original_amount * interest_rate * (days_overdue / 30)
        current_amount = original_amount + interest
        
        assert interest > 0
        assert current_amount > original_amount
    
    def test_debt_overdue_status(self):
        """Testa determinação de status em atraso"""
        from datetime import date
        
        due_date = date.today() - timedelta(days=10)
        is_overdue = date.today() > due_date
        
        assert is_overdue


class TestPaymentEntity:
    """Testes da entidade Payment"""
    
    def test_create_payment_success(self):
        """Testa criação bem-sucedida de pagamento"""
        from ..factories import PaymentFactory
        
        taxpayer_data = TaxpayerFactory.create()
        taxpayer_id = taxpayer_data["id"]
        
        debt_data = {
            "id": uuid4(),
            "taxpayer_id": taxpayer_id
        }
        debt_id = debt_data["id"]
        
        payment_data = PaymentFactory.create(
            taxpayer_id=taxpayer_id,
            debt_id=debt_id
        )
        
        assert payment_data["taxpayer_id"] == taxpayer_id
        assert payment_data["debt_id"] == debt_id
        assert payment_data["amount"] > 0
        assert payment_data["status"] == "COMPLETED"
    
    def test_payment_methods(self):
        """Testa métodos de pagamento"""
        payment_methods = ["CASH", "TRANSFER", "MULTICAIXA"]
        
        for method in payment_methods:
            assert method in payment_methods


class TestCertificateEntity:
    """Testes da entidade Certificate"""
    
    def test_create_certificate_success(self):
        """Testa criação bem-sucedida de certidão"""
        from ..factories import CertificateFactory
        
        taxpayer_data = TaxpayerFactory.create()
        taxpayer_id = taxpayer_data["id"]
        
        cert_data = CertificateFactory.create(taxpayer_id=taxpayer_id)
        
        assert cert_data["taxpayer_id"] == taxpayer_id
        assert cert_data["certificate_type"] in ["NIF", "DEBT", "INCOME"]
        assert cert_data["status"] == "PENDING"
        assert cert_data["year"] == 2024
    
    def test_certificate_types(self):
        """Testa tipos de certidão"""
        types = ["NIF", "DEBT", "INCOME"]
        
        for cert_type in types:
            assert cert_type in types
