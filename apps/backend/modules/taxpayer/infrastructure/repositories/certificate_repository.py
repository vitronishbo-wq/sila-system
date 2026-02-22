"""Certificate Repository Implementation"""

from typing import Optional, List, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import date

from ..models.tax_certificate_model import TaxCertificateModel
from .base_repository import BaseRepository


class CertificateRepository(BaseRepository[TaxCertificateModel]):
    """Repository for tax certificates"""
    
    def __init__(self, db: Session):
        super().__init__(db, TaxCertificateModel)
    
    def save(self, certificate_data: dict) -> TaxCertificateModel:
        """Save certificate"""
        existing = self.get_by_id(certificate_data.get('id'))
        if existing:
            for key, value in certificate_data.items():
                if value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            return existing
        else:
            return self.create(**certificate_data)
    
    def find_by_number(self, certificate_number: str) -> Optional[TaxCertificateModel]:
        """Find by certificate number"""
        return self.db.query(TaxCertificateModel).filter(
            TaxCertificateModel.certificate_number == certificate_number
        ).first()
    
    def find_by_taxpayer(self, taxpayer_id: UUID, certificate_type: Optional[str] = None,
                        skip: int = 0, limit: int = 100) -> Tuple[List[TaxCertificateModel], int]:
        """Find by taxpayer"""
        query = self.db.query(TaxCertificateModel).filter(
            TaxCertificateModel.taxpayer_id == taxpayer_id
        )
        
        if certificate_type:
            query = query.filter(TaxCertificateModel.certificate_type == certificate_type)
        
        total = query.count()
        models = query.order_by(desc(TaxCertificateModel.requested_at)).offset(skip).limit(limit).all()
        
        return models, total
    
    def find_valid(self, taxpayer_id: UUID, certificate_type: str) -> Optional[TaxCertificateModel]:
        """Find valid certificate"""
        today = date.today()
        model = self.db.query(TaxCertificateModel).filter(
            TaxCertificateModel.taxpayer_id == taxpayer_id,
            TaxCertificateModel.certificate_type == certificate_type,
            TaxCertificateModel.status == "ISSUED",
            TaxCertificateModel.expires_at >= today
        ).first()
        
        return model
    
    def find_by_type(self, certificate_type: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxCertificateModel], int]:
        """Find by certificate type"""
        query = self.db.query(TaxCertificateModel).filter(
            TaxCertificateModel.certificate_type == certificate_type
        )
        total = query.count()
        models = query.order_by(desc(TaxCertificateModel.requested_at)).offset(skip).limit(limit).all()
        return models, total
    
    def find_expired(self) -> List[TaxCertificateModel]:
        """Find expired certificates"""
        today = date.today()
        return self.db.query(TaxCertificateModel).filter(
            TaxCertificateModel.expires_at < today,
            TaxCertificateModel.status == "ISSUED"
        ).all()
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxCertificateModel], int]:
        """Find by status"""
        query = self.db.query(TaxCertificateModel).filter(
            TaxCertificateModel.status == status
        )
        total = query.count()
        models = query.order_by(desc(TaxCertificateModel.requested_at)).offset(skip).limit(limit).all()
        return models, total
