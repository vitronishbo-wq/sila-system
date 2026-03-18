"""Base repository abstrato para padrão de implementação."""
import logging
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

logger = logging.getLogger(__name__)

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Abstract Base Repository para padronizar implementações.
    
    Fornece pattern template para CRUD operations + domínio-específico.
    Subclasses devem implementar com SQLAlchemy ou outro ORM.
    """

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Cria nova entidade."""
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Salva/atualiza entidade existente."""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Recupera entidade por ID primário."""
        pass

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Lista todas as entidades com paginação."""
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Deleta entidade por ID."""
        pass

    @abstractmethod
    async def exists(self, entity_id: str) -> bool:
        """Verifica existência de entidade."""
        pass
