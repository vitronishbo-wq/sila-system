from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
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
    
    def get_all(self, skip: int = 0, limit: int = 100, order_by: str = "created_at") -> List[ModelType]:
        """Lista todos os registros ativos com paginação"""
        query = self.db.query(self.model_class).filter(self.model_class.is_active == True)
        if hasattr(self.model_class, order_by):
            query = query.order_by(desc(getattr(self.model_class, order_by)))
        return query.offset(skip).limit(limit).all()
    
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
            self.db.flush()
        return obj
    
    def delete(self, id: str, soft_delete: bool = True) -> bool:
        """Remove um registro (soft delete por padrão)"""
        obj = self.get_by_id(id)
        if obj:
            if soft_delete:
                obj.is_active = False
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
