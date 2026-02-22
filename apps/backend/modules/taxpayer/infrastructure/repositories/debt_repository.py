"""Debt Repository Implementation"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import date, datetime

from ..models.tax_debt_model import TaxDebtModel
from .base_repository import BaseRepository


class DebtRepository(BaseRepository[TaxDebtModel]):
    """Repository for tax debts"""
    
    def __init__(self, db: Session):
        super().__init__(db, TaxDebtModel)
    
    def save(self, debt_data: dict) -> TaxDebtModel:
        """Save debt"""
        existing = self.get_by_id(debt_data.get('id'))
        if existing:
            for key, value in debt_data.items():
                if value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            return existing
        else:
            return self.create(**debt_data)
    
    def find_by_number(self, debt_number: str) -> Optional[TaxDebtModel]:
        """Find by debt number"""
        return self.db.query(TaxDebtModel).filter(
            TaxDebtModel.debt_number == debt_number
        ).first()
    
    def find_by_taxpayer(self, taxpayer_id: UUID, include_paid: bool = False,
                        skip: int = 0, limit: int = 100) -> Tuple[List[TaxDebtModel], int]:
        """Find by taxpayer"""
        query = self.db.query(TaxDebtModel).filter(
            TaxDebtModel.taxpayer_id == taxpayer_id
        )
        
        if not include_paid:
            query = query.filter(TaxDebtModel.status.in_(["PENDING", "PARTIAL"]))
        
        total = query.count()
        models = query.order_by(TaxDebtModel.due_date).offset(skip).limit(limit).all()
        
        return models, total
    
    def find_overdue(self, reference_date: Optional[date] = None) -> List[TaxDebtModel]:
        """Find overdue debts"""
        if not reference_date:
            reference_date = date.today()
        
        models = self.db.query(TaxDebtModel).filter(
            TaxDebtModel.due_date < reference_date,
            TaxDebtModel.status.in_(["PENDING", "PARTIAL"])
        ).all()
        
        return models
    
    def update_after_payment(self, debt_id: UUID, payment_amount: float) -> Optional[TaxDebtModel]:
        """Update debt after payment"""
        debt = self.get_by_id(debt_id)
        if not debt:
            return None
        
        new_balance = float(debt.current_amount) - payment_amount
        
        updates = {
            "current_amount": max(new_balance, 0)
        }
        
        if new_balance <= 0:
            updates["status"] = "PAID"
            updates["paid_at"] = datetime.now()
        else:
            updates["status"] = "PARTIAL"
        
        return self.update(debt_id, **updates)
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxDebtModel], int]:
        """Find by status"""
        query = self.db.query(TaxDebtModel).filter(TaxDebtModel.status == status)
        total = query.count()
        models = query.order_by(TaxDebtModel.due_date).offset(skip).limit(limit).all()
        return models, total
