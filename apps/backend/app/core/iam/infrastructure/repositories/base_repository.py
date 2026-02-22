from typing import TypeVar, Generic, Type, Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime

from ..models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Repositório base com operações CRUD comuns"""
    
    def __init__(self, db: Session, model_class: Type[ModelType]):
        self.db = db
        self.model_class = model_class
    
    def get_by_id(self, id: str) -> Optional[ModelType]:
        """Busca por ID"""
        return self.db.query(self.model_class).filter(
            self.model_class.id == id,
            self.model_class.is_active == True
        ).first()
    
    def get_by_ids(self, ids: List[str]) -> List[ModelType]:
        """Busca múltiplos IDs"""
        return self.db.query(self.model_class).filter(
            self.model_class.id.in_(ids),
            self.model_class.is_active == True
        ).all()
    
    def get_all(self, skip: int = 0, limit: int = 100, 
                order_by: str = "created_at", descending: bool = True) -> Tuple[List[ModelType], int]:
        """Lista todos os registros ativos com paginação"""
        query = self.db.query(self.model_class).filter(self.model_class.is_active == True)
        
        # Total count
        total = query.count()
        
        # Order by
        if hasattr(self.model_class, order_by):
            order_column = getattr(self.model_class, order_by)
            if descending:
                query = query.order_by(desc(order_column))
            else:
                query = query.order_by(order_column)
        
        # Pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    def create(self, **kwargs) -> ModelType:
        """Cria um novo registro"""
        obj = self.model_class(**kwargs)
        self.db.add(obj)
        self.db.flush()
        return obj
    
    def update(self, id: str, **kwargs) -> Optional[ModelType]:
        """Atualiza um registro"""
        obj = self.get_by_id(id)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key) and value is not None:
                    setattr(obj, key, value)
            obj.updated_at = datetime.now()
            self.db.flush()
        return obj
    
    def delete(self, id: str, soft_delete: bool = True) -> bool:
        """Remove um registro (soft delete por padrão)"""
        obj = self.get_by_id(id)
        if obj:
            if soft_delete:
                obj.is_active = False
                obj.updated_at = datetime.now()
                self.db.flush()
            else:
                self.db.delete(obj)
                self.db.flush()
            return True
        return False
    
    def exists(self, **filters) -> bool:
        """Verifica se existe registro com os filtros"""
        query = self.db.query(self.model_class).filter_by(**filters)
        return query.first() is not None
    
    def count(self, **filters) -> int:
        """Conta registros com filtros"""
        query = self.db.query(self.model_class).filter_by(**filters)
        return query.count()
    
    def find_by(self, **filters) -> List[ModelType]:
        """Busca por filtros exatos"""
        return self.db.query(self.model_class).filter_by(**filters).all()
    
    def find_one_by(self, **filters) -> Optional[ModelType]:
        """Busca um registro por filtros exatos"""
        return self.db.query(self.model_class).filter_by(**filters).first()
    
    def bulk_create(self, items: List[Dict[str, Any]]) -> List[ModelType]:
        """Cria múltiplos registros"""
        objects = [self.model_class(**item) for item in items]
        self.db.add_all(objects)
        self.db.flush()
        return objects
    
    def bulk_update(self, items: List[ModelType]) -> List[ModelType]:
        """Atualiza múltiplos registros"""
        for item in items:
            item.updated_at = datetime.now()
        self.db.flush()
        return items
