"""
Factories para criar dados de teste
"""
from typing import Dict, Any, Optional
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
import random


class TaxpayerFactory:
    """Factory para criar contribuintes de teste"""
    
    @staticmethod
    def create(
        nif: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        status: str = "ACTIVE",
        **kwargs
    ) -> Dict[str, Any]:
        """Cria dados de contribuinte"""
        if not nif:
            nif = f"{random.randint(100000000, 999999999)}"
        
        if not name:
            name = f"Contribuinte Teste {nif[-4:]}"
        
        if not email:
            email = f"test{nif[-4:]}@example.com"
        
        return {
            "id": kwargs.get("id", uuid4()),
            "nif": nif,
            "name": name,
            "email": email,
            "phone": f"+244923{nif[-4:]}",
            "address": f"Rua Teste, {random.randint(1, 1000)}, Luanda",
            "tax_regime": kwargs.get("tax_regime", "GERAL"),
            "status": status,
            "registered_by": kwargs.get("registered_by", uuid4()),
            "registered_at": kwargs.get("registered_at", datetime.now() - timedelta(days=30)),
            "updated_at": kwargs.get("updated_at", None),
            "updated_by": kwargs.get("updated_by", None),
        }


class DeclarationFactory:
    """Factory para criar declarações de teste"""
    
    @staticmethod
    def create(
        taxpayer_id: UUID,
        tax_type: str = "IVA",
        status: str = "PENDING",
        **kwargs
    ) -> Dict[str, Any]:
        """Cria dados de declaração"""
        year = kwargs.get("year", 2024)
        month = kwargs.get("month", random.randint(1, 12))
        period = f"{year}-{month:02d}"
        
        gross = kwargs.get("gross_amount", random.uniform(100000, 1000000))
        deductions = kwargs.get("deductions", gross * 0.15)
        net = gross - deductions
        
        return {
            "id": kwargs.get("id", uuid4()),
            "taxpayer_id": taxpayer_id,
            "declaration_number": f"DEC/{year}/{random.randint(1, 999999):06d}",
            "tax_type": tax_type,
            "tax_period": period,
            "gross_amount": gross,
            "deductions": deductions,
            "net_amount": net,
            "declaration_date": kwargs.get("declaration_date", date(year, month, 15)),
            "due_date": kwargs.get("due_date", date(year, month, 28)),
            "status": status,
            "submitted_by": kwargs.get("submitted_by", uuid4()),
            "submitted_at": kwargs.get("submitted_at", datetime.now()),
        }


class DebtFactory:
    """Factory para criar dívidas de teste"""
    
    @staticmethod
    def create(
        taxpayer_id: UUID,
        status: str = "PENDING",
        **kwargs
    ) -> Dict[str, Any]:
        """Cria dados de dívida"""
        year = kwargs.get("year", 2024)
        month = kwargs.get("month", random.randint(1, 12))
        
        original = kwargs.get("original_amount", random.uniform(50000, 500000))
        days_overdue = kwargs.get("days_overdue", 0)
        interest = original * 0.01 * (days_overdue / 30)
        
        return {
            "id": kwargs.get("id", uuid4()),
            "taxpayer_id": taxpayer_id,
            "debt_number": f"DEBT/{year}/{random.randint(1, 999999):06d}",
            "tax_type": kwargs.get("tax_type", "IVA"),
            "original_amount": original,
            "current_amount": original + interest,
            "interest": interest,
            "fines": kwargs.get("fines", 0),
            "created_date": kwargs.get("created_date", date(year, month, 1)),
            "due_date": kwargs.get("due_date", date(year, month, 28) + timedelta(days=days_overdue)),
            "status": status,
        }


class PaymentFactory:
    """Factory para criar pagamentos de teste"""
    
    @staticmethod
    def create(
        taxpayer_id: UUID,
        debt_id: UUID,
        **kwargs
    ) -> Dict[str, Any]:
        """Cria dados de pagamento"""
        year = kwargs.get("year", 2024)
        amount = kwargs.get("amount", random.uniform(1000, 100000))
        
        return {
            "id": kwargs.get("id", uuid4()),
            "taxpayer_id": taxpayer_id,
            "debt_id": debt_id,
            "payment_number": f"PAY/{year}/{random.randint(1, 99999999):08d}",
            "amount": amount,
            "payment_method": kwargs.get("payment_method", random.choice(["CASH", "TRANSFER", "MULTICAIXA"])),
            "payment_date": kwargs.get("payment_date", datetime.now() - timedelta(days=random.randint(1, 30))),
            "status": kwargs.get("status", "COMPLETED"),
            "reference": kwargs.get("reference", f"REF-{random.randint(1000, 9999)}"),
            "paid_by": kwargs.get("paid_by", uuid4()),
        }


class CertificateFactory:
    """Factory para criar certidões de teste"""
    
    @staticmethod
    def create(
        taxpayer_id: UUID,
        **kwargs
    ) -> Dict[str, Any]:
        """Cria dados de certidão"""
        year = kwargs.get("year", 2024)
        
        return {
            "id": kwargs.get("id", uuid4()),
            "taxpayer_id": taxpayer_id,
            "certificate_number": f"CERT/{year}/{random.randint(1, 99999999):08d}",
            "certificate_type": kwargs.get("certificate_type", random.choice(["NIF", "DEBT", "INCOME"])),
            "year": year,
            "status": kwargs.get("status", "PENDING"),
            "requested_by": kwargs.get("requested_by", uuid4()),
            "requested_at": kwargs.get("requested_at", datetime.now() - timedelta(days=random.randint(1, 5))),
            "expires_at": kwargs.get("expires_at", date(year, 12, 31)),
        }
