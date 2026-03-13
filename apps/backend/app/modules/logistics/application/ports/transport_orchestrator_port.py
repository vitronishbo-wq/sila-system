"""Unified Transport Port"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import List, Optional

class TransportModality(str, Enum):
    RODOVIARIO = "rodoviario"
    FERROVIARIO = "ferroviario"
    MARITIMO = "maritimo"
    AEREO = "aereo"

class RotaStatus(str, Enum):
    PLANEJADA = "planejada"
    ATIVA = "ativa"
    SUSPENSA = "suspensa"

@dataclass
class Rota:
    rota_id: str
    nome: str
    modalidade: TransportModality
    distancia_km: Decimal
    custo_operacional: Decimal

class TransportOrchestratorPort(ABC):
    """Unified transport orchestration interface"""
    @abstractmethod
    async def registrar_rota(self, rota: Rota):
        pass
