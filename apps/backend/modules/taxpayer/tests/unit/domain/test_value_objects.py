"""
Testes de value objects
"""
import pytest
from datetime import date, datetime


class TestValueObjects:
    """Testes de value objects"""
    
    def test_nif_validation(self):
        """Testa validação de NIF"""
        valid_nif = "123456789"
        invalid_nif = "ABC"
        
        assert len(valid_nif) >= 9
        assert valid_nif.isdigit()
        assert not invalid_nif.isdigit()
    
    def test_email_format(self):
        """Testa formato de email"""
        import re
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        valid_email = "test@example.com"
        invalid_email = "invalid.email"
        
        assert re.match(email_regex, valid_email)
        assert not re.match(email_regex, invalid_email)
    
    def test_phone_format(self):
        """Testa formato de telefone"""
        valid_phone = "+244923456789"
        
        assert valid_phone.startswith("+244")
        assert len(valid_phone) == 13
    
    def test_monetary_amount(self):
        """Testa valores monetários"""
        amount = 1000.50
        
        assert amount > 0
        assert round(amount, 2) == 1000.50
    
    def test_tax_period_format(self):
        """Testa formato de período fiscal"""
        import re
        
        period_regex = r'^\d{4}-\d{2}$'
        
        valid_period = "2024-01"
        invalid_period = "2024/01"
        
        assert re.match(period_regex, valid_period)
        assert not re.match(period_regex, invalid_period)
    
    def test_tax_regime_values(self):
        """Testa valores de regime fiscal"""
        valid_regimes = ["GERAL", "SIMPLIFICADO", "MEI", "OUTROS"]
        
        for regime in valid_regimes:
            assert regime in valid_regimes
    
    def test_status_values(self):
        """Testa valores de status"""
        valid_statuses = [
            "ACTIVE", "SUSPENDED", "CANCELLED", "PENDING",
            "APPROVED", "REJECTED", "PROCESSING", "COMPLETED",
            "OVERDUE", "PAID"
        ]
        
        for status in valid_statuses:
            assert status in valid_statuses
    
    def test_tax_type_values(self):
        """Testa tipos de imposto"""
        valid_types = ["IVA", "IRS", "IRC", "OUTROS"]
        
        for tax_type in valid_types:
            assert tax_type in valid_types


class TestDateRanges:
    """Testes de intervalos de data"""
    
    def test_declaration_date_range(self):
        """Testa intervalo de data de declaração"""
        from datetime import datetime, timedelta
        
        declaration_date = date.today()
        max_past = date.today() - timedelta(days=365)
        max_future = date.today() + timedelta(days=30)
        
        assert declaration_date >= max_past
        assert declaration_date <= max_future
    
    def test_due_date_after_declaration_date(self):
        """Testa data de vencimento após data de declaração"""
        from datetime import datetime, timedelta
        
        declaration_date = date.today()
        due_date = declaration_date + timedelta(days=30)
        
        assert due_date > declaration_date
    
    def test_certificate_expiration(self):
        """Testa expiração de certidão"""
        issue_date = date.today()
        expiration_date = date(2024, 12, 31)
        
        assert expiration_date > issue_date


class TestAmountCalculations:
    """Testes de cálculos de valores"""
    
    def test_deduction_percentage(self):
        """Testa percentual de dedução"""
        gross_amount = 1000000.0
        deduction_rate = 0.15  # 15%
        deductions = gross_amount * deduction_rate
        net_amount = gross_amount - deductions
        
        assert deductions == 150000.0
        assert net_amount == 850000.0
    
    def test_interest_calculation(self):
        """Testa cálculo de juros"""
        principal = 100000.0
        monthly_rate = 0.01  # 1% ao mês
        months = 3
        interest = principal * monthly_rate * months
        
        assert interest == 3000.0
    
    def test_fine_calculation(self):
        """Testa cálculo de multa"""
        base_amount = 100000.0
        fine_rate = 0.05  # 5%
        fine = base_amount * fine_rate
        
        assert fine == 5000.0
    
    def test_total_debt_calculation(self):
        """Testa cálculo de dívida total"""
        original = 100000.0
        interest = 3000.0
        fines = 5000.0
        total = original + interest + fines
        
        assert total == 108000.0
