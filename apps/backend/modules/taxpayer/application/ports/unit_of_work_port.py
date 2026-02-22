from abc import ABC, abstractmethod
from typing import Optional


class UnitOfWorkPort(ABC):
    """Interface para Unit of Work - transaction boundary"""
    
    @abstractmethod
    async def begin(self) -> None:
        """Inicia transação"""
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """Confirma transação"""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Reverte transação"""
        pass
    
    @abstractmethod
    async def __aenter__(self):
        """Context manager entry"""
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - auto-rollback on exception"""
        pass
