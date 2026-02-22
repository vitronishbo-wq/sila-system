"""Declaration Repository Implementation"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, extract
from datetime import datetime, date

from ..models.tax_declaration_model import TaxDeclarationModel
from .base_repository import BaseRepository


class DeclarationRepository(BaseRepository[TaxDeclarationModel]):
    """Repository for tax declarations"""
    
    def __init__(self, db: Session):
        super().__init__(db, TaxDeclarationModel)
    
    def save(self, declaration_data: dict) -> TaxDeclarationModel:
        """Save declaration"""
        existing = self.get_by_id(declaration_data.get('id'))
        if existing:
            for key, value in declaration_data.items():
                if value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            return existing
        else:
            return self.create(**declaration_data)
    
    def find_by_number(self, declaration_number: str) -> Optional[TaxDeclarationModel]:
        """Find by declaration number"""
        return self.db.query(TaxDeclarationModel).filter(
            TaxDeclarationModel.declaration_number == declaration_number
        ).first()
    
    def find_by_taxpayer(self, taxpayer_id: UUID, year: Optional[int] = None,
                        skip: int = 0, limit: int = 100) -> Tuple[List[TaxDeclarationModel], int]:
        """Find by taxpayer"""
        query = self.db.query(TaxDeclarationModel).filter(
            TaxDeclarationModel.taxpayer_id == taxpayer_id
        )
        
        if year:
            query = query.filter(
                extract('year', TaxDeclarationModel.declaration_date) == year
            )
        
        total = query.count()
        models = query.order_by(desc(TaxDeclarationModel.declaration_date)).offset(skip).limit(limit).all()
        
        return models, total
    
    def find_by_period(self, tax_type: str, year: int, month: Optional[int] = None) -> List[TaxDeclarationModel]:
        """Find by period"""
        query = self.db.query(TaxDeclarationModel).filter(
            TaxDeclarationModel.tax_type == tax_type,
            extract('year', TaxDeclarationModel.declaration_date) == year
        )
        
        if month:
            query = query.filter(extract('month', TaxDeclarationModel.declaration_date) == month)
        
        return query.all()
    
    def update_status(self, declaration_id: UUID, status: str, processed_by: Optional[UUID] = None) -> Optional[TaxDeclarationModel]:
        """Update declaration status"""
        updates = {
            "status": status,
            "processed_at": datetime.now()
        }
        if processed_by:
            updates["processed_by"] = processed_by
        
        return self.update(declaration_id, **updates)
    
    def find_pending(self, skip: int = 0, limit: int = 100) -> Tuple[List[TaxDeclarationModel], int]:
        """Find pending declarations"""
        query = self.db.query(TaxDeclarationModel).filter(
            TaxDeclarationModel.status == "PENDING"
        )
        total = query.count()
        models = query.order_by(TaxDeclarationModel.due_date).offset(skip).limit(limit).all()
        return models, total
