"""Taxpayer Repository Implementation"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
from datetime import datetime

from ..models.taxpayer_model import TaxpayerModel
from .base_repository import BaseRepository


class TaxpayerRepository(BaseRepository[TaxpayerModel]):
    """Repository for taxpayers"""
    
    def __init__(self, db: Session):
        super().__init__(db, TaxpayerModel)
    
    def save(self, taxpayer_data: dict) -> TaxpayerModel:
        """Save a taxpayer"""
        existing = self.get_by_id(taxpayer_data.get('id'))
        if existing:
            for key, value in taxpayer_data.items():
                if value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            return existing
        else:
            return self.create(**taxpayer_data)
    
    def find_by_nif(self, nif: str) -> Optional[TaxpayerModel]:
        """Find by NIF"""
        return self.db.query(TaxpayerModel).filter(
            TaxpayerModel.nif == nif
        ).first()
    
    def find_by_email(self, email: str) -> Optional[TaxpayerModel]:
        """Find by email"""
        return self.db.query(TaxpayerModel).filter(
            TaxpayerModel.email == email
        ).first()
    
    def find_by_phone(self, phone: str) -> Optional[TaxpayerModel]:
        """Find by phone"""
        return self.db.query(TaxpayerModel).filter(
            TaxpayerModel.phone == phone
        ).first()
    
    def list_all(self, skip: int = 0, limit: int = 100, filters: dict = None) -> Tuple[List[TaxpayerModel], int]:
        """List all taxpayers"""
        models, total = self.get_all(skip, limit, "registered_at", True, filters)
        return models, total
    
    def update_status(self, taxpayer_id: UUID, status: str, updated_by: UUID) -> Optional[TaxpayerModel]:
        """Update taxpayer status"""
        return self.update(taxpayer_id, status=status, updated_by=updated_by, updated_at=datetime.now())
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxpayerModel], int]:
        """Find by status"""
        query = self.db.query(TaxpayerModel).filter(TaxpayerModel.status == status)
        total = query.count()
        models = query.order_by(desc(TaxpayerModel.registered_at)).offset(skip).limit(limit).all()
        return models, total
    
    def find_by_regime(self, tax_regime: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxpayerModel], int]:
        """Find by tax regime"""
        query = self.db.query(TaxpayerModel).filter(TaxpayerModel.tax_regime == tax_regime)
        total = query.count()
        models = query.offset(skip).limit(limit).all()
        return models, total
    
    def search(self, query_str: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxpayerModel], int]:
        """Search taxpayers"""
        query = self.db.query(TaxpayerModel).filter(
            or_(
                TaxpayerModel.nif.ilike(f"%{query_str}%"),
                TaxpayerModel.name.ilike(f"%{query_str}%"),
                TaxpayerModel.email.ilike(f"%{query_str}%")
            )
        )
        total = query.count()
        models = query.offset(skip).limit(limit).all()
        return models, total
