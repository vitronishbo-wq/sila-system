from abc import ABC, abstractmethod
from typing import List
from app.modules.justice.bounded_contexts.infrastructure.models.cemetery_inspection_record import CemeteryInspectionRecord

class CemeteryInspectionRepositoryPort(ABC):
    """Porta (Interface) para o Repositório de Inspeções de Cemitérios."""

    @abstractmethod
    async def save(self, inspection: CemeteryInspectionRecord) -> CemeteryInspectionRecord:
        pass

    @abstractmethod
    async def list_by_cemetery(self, cemetery_name: str) -> List[CemeteryInspectionRecord]:
        pass