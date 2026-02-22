"""Base Repository with common CRUD operations"""

from typing import TypeVar, Generic, Type, Optional, List, Tuple
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

# Try importing Base, if not available use declarative_base
try:
    from ....core.database import Base
except ImportError:
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations"""
    
    def __init__(self, db: Session, model_class: Type[ModelType]):
        self.db = db
        self.model_class = model_class
    
    def get_by_id(self, id: UUID) -> Optional[ModelType]:
        """Get by ID"""
        return self.db.query(self.model_class).filter(
            self.model_class.id == id
        ).first()
    
    def get_by_ids(self, ids: List[UUID]) -> List[ModelType]:
        """Get multiple by IDs"""
        return self.db.query(self.model_class).filter(
            self.model_class.id.in_(ids)
        ).all()
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                order_by: str = "created_at", descending: bool = True,
                filters: dict = None) -> Tuple[List[ModelType], int]:
        """List all with pagination"""
        query = self.db.query(self.model_class)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model_class, key) and value is not None:
                    query = query.filter(getattr(self.model_class, key) == value)
        
        total = query.count()
        
        if hasattr(self.model_class, order_by):
            order_column = getattr(self.model_class, order_by)
            if descending:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(order_column)
        
        items = query.offset(skip).limit(limit).all()
        return items, total
    
    def create(self, **kwargs) -> ModelType:
        """Create new record"""
        obj = self.model_class(**kwargs)
        self.db.add(obj)
        self.db.flush()
        return obj
    
    def update(self, id: UUID, **kwargs) -> Optional[ModelType]:
        """Update record"""
        obj = self.get_by_id(id)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key) and value is not None:
                    setattr(obj, key, value)
            if hasattr(obj, 'updated_at'):
                obj.updated_at = datetime.now()
            self.db.flush()
        return obj
    
    def delete(self, id: UUID, soft_delete: bool = False) -> bool:
        """Delete record"""
        obj = self.get_by_id(id)
        if obj:
            if soft_delete and hasattr(obj, 'is_active'):
                obj.is_active = False
                obj.updated_at = datetime.now()
            else:
                self.db.delete(obj)
            self.db.flush()
            return True
        return False
    
    def exists(self, **filters) -> bool:
        """Check if exists"""
        return self.db.query(self.model_class).filter_by(**filters).first() is not None
    
    def count(self, **filters) -> int:
        """Count records"""
        return self.db.query(self.model_class).filter_by(**filters).count()
    
    def find_by(self, **filters) -> List[ModelType]:
        """Find by exact filters"""
        return self.db.query(self.model_class).filter_by(**filters).all()
    
    def find_one_by(self, **filters) -> Optional[ModelType]:
        """Find one record by filters"""
        return self.db.query(self.model_class).filter_by(**filters).first()
