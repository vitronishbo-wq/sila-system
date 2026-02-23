from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
import uuid

# Usar o Base centralizado
from app.core.database import Base


class BaseModel(Base):
    """Classe base para todos os modelos IAM"""
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(36), nullable=True)
    updated_by = Column(String(36), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def to_dict(self):
        """Converte modelo para dicionário"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    def to_dict_safe(self, exclude_fields: list = None):
        """Converte para dicionário excluindo campos sensíveis"""
        exclude = exclude_fields or []
        result = {}
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                result[column.name] = value
        return result
