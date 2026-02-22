"""Audit Repository Implementation"""

from typing import Optional, List, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime

from ..models.tax_audit_model import TaxAuditModel
from .base_repository import BaseRepository


class AuditRepository(BaseRepository[TaxAuditModel]):
    """Repository for audit logs"""
    
    def __init__(self, db: Session):
        super().__init__(db, TaxAuditModel)
    
    def store(self, action: str, user_id: Optional[UUID], entity_id: Optional[UUID],
             entity_type: str, details: Dict[str, Any], ip_address: Optional[str] = None,
             user_agent: Optional[str] = None) -> TaxAuditModel:
        """Store audit log"""
        audit = self.create(
            action=action,
            user_id=user_id,
            entity_id=entity_id,
            entity_type=entity_type,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        self.db.flush()
        return audit
    
    def get_by_entity(self, entity_type: str, entity_id: UUID, limit: int = 100) -> List[TaxAuditModel]:
        """Find all logs for entity"""
        return self.db.query(TaxAuditModel).filter(
            TaxAuditModel.entity_type == entity_type,
            TaxAuditModel.entity_id == entity_id
        ).order_by(desc(TaxAuditModel.created_at)).limit(limit).all()
    
    def get_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> Tuple[List[TaxAuditModel], int]:
        """Find all logs by user"""
        query = self.db.query(TaxAuditModel).filter(TaxAuditModel.user_id == user_id)
        total = query.count()
        models = query.order_by(desc(TaxAuditModel.created_at)).offset(skip).limit(limit).all()
        return models, total
    
    def get_by_action(self, action: str, skip: int = 0, limit: int = 100) -> Tuple[List[TaxAuditModel], int]:
        """Find all logs by action"""
        query = self.db.query(TaxAuditModel).filter(TaxAuditModel.action == action)
        total = query.count()
        models = query.order_by(desc(TaxAuditModel.created_at)).offset(skip).limit(limit).all()
        return models, total
    
    def search(self, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> Tuple[List[TaxAuditModel], int]:
        """Search audit logs"""
        query = self.db.query(TaxAuditModel)
        
        if filters.get('user_id'):
            query = query.filter(TaxAuditModel.user_id == filters['user_id'])
        if filters.get('entity_id'):
            query = query.filter(TaxAuditModel.entity_id == filters['entity_id'])
        if filters.get('entity_type'):
            query = query.filter(TaxAuditModel.entity_type == filters['entity_type'])
        if filters.get('action'):
            query = query.filter(TaxAuditModel.action == filters['action'])
        if filters.get('start_date'):
            query = query.filter(TaxAuditModel.created_at >= filters['start_date'])
        if filters.get('end_date'):
            query = query.filter(TaxAuditModel.created_at <= filters['end_date'])
        
        total = query.count()
        models = query.order_by(desc(TaxAuditModel.created_at)).offset(skip).limit(limit).all()
        return models, total
    
    def get_recent(self, limit: int = 100) -> List[TaxAuditModel]:
        """Get recent audit entries"""
        return self.db.query(TaxAuditModel).order_by(
            desc(TaxAuditModel.created_at)
        ).limit(limit).all()
