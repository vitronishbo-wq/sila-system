from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import timedelta


class CachePort(ABC):
    """Interface para cache"""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: timedelta = timedelta(minutes=5)):
        """Armazena valor no cache"""
        pass
    
    @abstractmethod
    async def delete(self, key: str):
        """Remove valor do cache"""
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Verifica se chave existe"""
        pass
    
    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        """Incrementa valor"""
        pass
    
    @abstractmethod
    async def expire(self, key: str, ttl: timedelta):
        """Define tempo de expiração"""
        pass
    
    @abstractmethod
    async def clear_pattern(self, pattern: str):
        """Remove todas as chaves com padrão"""
        pass
    
    @abstractmethod
    async def get_or_set(self, key: str, fallback, ttl: timedelta = timedelta(minutes=5)) -> Any:
        """Obtém do cache ou executa fallback"""
        pass
