from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from apps.backend.app.modules.society.cultura.domain.enums import CategoriaPatrimonioImaterial, StatusPatrimonioImaterial
from apps.backend.app.modules.society.cultura.domain.models.patrimonio_imaterial import PatrimonioImaterial

class PatrimonioImaterialRepositoryPort(ABC):

    @abstractmethod
    async def save(self, patrimonio: PatrimonioImaterial) -> PatrimonioImaterial:
        pass

    @abstractmethod
    async def get_by_id(self, patrimonio_id: UUID) -> PatrimonioImaterial | None:
        pass

    @abstractmethod
    async def get_by_registro(self, registro_pni: str) -> PatrimonioImaterial | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[PatrimonioImaterial]:
        pass

    @abstractmethod
    async def list_by_categoria(self, categoria: CategoriaPatrimonioImaterial) -> list[PatrimonioImaterial]:
        pass

    @abstractmethod
    async def list_by_municipio(self, municipio: str) -> list[PatrimonioImaterial]:
        pass

    @abstractmethod
    async def list_by_status(self, status: StatusPatrimonioImaterial) -> list[PatrimonioImaterial]:
        pass

    @abstractmethod
    async def delete(self, patrimonio_id: UUID) -> bool:
        pass

    @abstractmethod
    async def next_registro(self) -> str:
        pass