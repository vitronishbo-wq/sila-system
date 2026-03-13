from __future__ import annotations
from abc import ABC, abstractmethod
from app.modules.resources.agricultura.domain.enums import StatusCertificacao
from app.modules.resources.agricultura.domain.models.certificacao import Certificacao

class CertificacaoRepositoryPort(ABC):

    @abstractmethod
    async def save(self, item: Certificacao) -> Certificacao:
        pass

    @abstractmethod
    async def get_by_codigo(self, codigo_certificacao: str) -> Certificacao | None:
        pass

    @abstractmethod
    async def list(self, *, codigo_propriedade: str | None=None, status: StatusCertificacao | None=None) -> list[Certificacao]:
        pass

    @abstractmethod
    async def next_codigo(self) -> str:
        pass