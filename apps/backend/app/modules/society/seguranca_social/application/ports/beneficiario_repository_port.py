from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.modules.society.seguranca_social.domain.enums import EstadoBeneficiario, RegimeSegurancaSocial, TipoBeneficiario
from app.modules.society.seguranca_social.domain.models.beneficiario import Beneficiario

class BeneficiarioRepositoryPort(ABC):

    @abstractmethod
    async def save(self, beneficiario: Beneficiario) -> Beneficiario:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Optional[Beneficiario]:
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: UUID) -> Optional[Beneficiario]:
        pass

    @abstractmethod
    async def get_by_numero(self, numero_beneficiario: str) -> Optional[Beneficiario]:
        pass

    @abstractmethod
    async def list_by_filtros(self, *, tipo: Optional[TipoBeneficiario]=None, estado: Optional[EstadoBeneficiario]=None, regime: Optional[RegimeSegurancaSocial]=None) -> list[Beneficiario]:
        pass

    @abstractmethod
    async def next_numero_beneficiario(self, ano: int) -> str:
        """Generate next id in format BEN/ANO/SEQUENCIAL."""
        pass