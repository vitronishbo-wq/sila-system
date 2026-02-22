"""Payment Repository Implementation"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from ..models.tax_payment_model import TaxPaymentModel
from .base_repository import BaseRepository


class PaymentRepository(BaseRepository[TaxPaymentModel]):
    """Repository for tax payments"""
    
    def __init__(self, db: Session):
        super().__init__(db, TaxPaymentModel)
    
    def save(self, payment_data: dict) -> TaxPaymentModel:
        """Save payment"""
        existing = self.get_by_id(payment_data.get('id'))
        if existing:
            for key, value in payment_data.items():
                if value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            return existing
        else:
            return self.create(**payment_data)
    
    def find_by_number(self, payment_number: str) -> Optional[TaxPaymentModel]:
        """Find by payment number"""
        return self.db.query(TaxPaymentModel).filter(
            TaxPaymentModel.payment_number == payment_number
        ).first()
    
    def find_by_taxpayer(self, taxpayer_id: UUID, skip: int = 0, limit: int = 100) -> Tuple[List[TaxPaymentModel], int]:
        """Find by taxpayer"""
        query = self.db.query(TaxPaymentModel).filter(
            TaxPaymentModel.taxpayer_id == taxpayer_id
        )
        total = query.count()
        models = query.order_by(desc(TaxPaymentModel.payment_date)).offset(skip).limit(limit).all()
        return models, total
    
    def find_by_debt(self, debt_id: UUID) -> List[TaxPaymentModel]:
        """Find by debt"""
        return self.db.query(TaxPaymentModel).filter(
            TaxPaymentModel.debt_id == debt_id
        ).order_by(TaxPaymentModel.payment_date).all()
    
    def find_by_reference(self, reference: str) -> Optional[TaxPaymentModel]:
        """Find by reference"""
        return self.db.query(TaxPaymentModel).filter(
            TaxPaymentModel.reference == reference
        ).first()
    
    def find_by_method(self, method: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxPaymentModel], int]:
        """Find by payment method"""
        query = self.db.query(TaxPaymentModel).filter(
            TaxPaymentModel.payment_method == method
        )
        total = query.count()
        models = query.order_by(desc(TaxPaymentModel.payment_date)).offset(skip).limit(limit).all()
        return models, total
