from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from typing import Callable, Type
from functools import wraps

from ...application.ports.unit_of_work_port import UnitOfWorkPort, UnitOfWorkFactoryPort
from ..database import SessionLocal


class SQLAlchemyUnitOfWork(UnitOfWorkPort):
    """Implementação SQLAlchemy do Unit of Work"""
    
    def __init__(self, session: Session):
        self.session = session
        self._closed = False
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()
    
    def commit(self):
        """Confirma transação"""
        if not self._closed:
            self.session.commit()
    
    def rollback(self):
        """Desfaz transação"""
        if not self._closed:
            self.session.rollback()
    
    def flush(self):
        """Flush para o banco sem commit"""
        if not self._closed:
            self.session.flush()
    
    def close(self):
        """Fecha a sessão"""
        if not self._closed:
            self.session.close()
            self._closed = True


class UnitOfWorkFactory(UnitOfWorkFactoryPort):
    """Factory para criar Unit of Work"""
    
    def create(self) -> UnitOfWorkPort:
        """Cria nova Unit of Work"""
        session = SessionLocal()
        return SQLAlchemyUnitOfWork(session)
    
    def transactional(self, func: Callable) -> Callable:
        """Decorator para tornar função transactional"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.create() as uow:
                result = func(*args, **kwargs, uow=uow)
                return result
        return wrapper
