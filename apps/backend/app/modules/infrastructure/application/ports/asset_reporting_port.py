"""Infrastructure Asset Reporting Port"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class AssetType(StrEnum):
    OBRA_PUBLICA = "obra_publica"
    MANUTENCAO = "manutencao"
    UTILIDADE = "utilidade"


class AssetStatus(StrEnum):
    PLANEJAMENTO = "planejamento"
    CONSTRUCAO = "construcao"
    OPERACIONAL = "operacional"
    MANUTENCAO = "manutencao"
    ENCERRADO = "encerrado"


@dataclass
class InfrastructureAsset:
    asset_id: str
    nome: str
    valor_atual: Decimal
    responsavel_did: str


class AssetReportingPort(ABC):
    """Abstract port for reporting assets to Treasury"""

    @abstractmethod
    async def register_asset(self, asset: InfrastructureAsset):
        pass
