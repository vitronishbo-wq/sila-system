from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=_utcnow)
    version: int = 1
    event_name: str = 'DomainEvent'

    def _base_payload(self) -> dict:
        return {'event_id': str(self.event_id), 'occurred_at': self.occurred_at.isoformat(), 'version': self.version}

    def to_payload(self) -> dict:
        return self._base_payload()

@dataclass(frozen=True)
class ObraCriadaEvent(DomainEvent):
    obra_id: str = ''
    codigo_obra: str = ''
    municipio: str = ''
    provincia: str = ''
    valor_orcado: str = '0.00'
    event_name: str = 'ObraCriadaEvent'

    @classmethod
    def build(cls, *, obra_id: UUID, codigo_obra: str, municipio: str, provincia: str, valor_orcado: Decimal) -> 'ObraCriadaEvent':
        return cls(obra_id=str(obra_id), codigo_obra=codigo_obra, municipio=municipio, provincia=provincia, valor_orcado=str(valor_orcado))

    def to_payload(self) -> dict:
        return {**self._base_payload(), 'obra_id': self.obra_id, 'codigo_obra': self.codigo_obra, 'municipio': self.municipio, 'provincia': self.provincia, 'valor_orcado': self.valor_orcado}

@dataclass(frozen=True)
class ObraIniciadaEvent(DomainEvent):
    obra_id: str = ''
    codigo_obra: str = ''
    data_inicio: str = ''
    event_name: str = 'ObraIniciadaEvent'

    @classmethod
    def build(cls, *, obra_id: UUID, codigo_obra: str, data_inicio: datetime | str) -> 'ObraIniciadaEvent':
        data_inicio_str = data_inicio.isoformat() if hasattr(data_inicio, 'isoformat') else str(data_inicio)
        return cls(obra_id=str(obra_id), codigo_obra=codigo_obra, data_inicio=data_inicio_str)

    def to_payload(self) -> dict:
        return {**self._base_payload(), 'obra_id': self.obra_id, 'codigo_obra': self.codigo_obra, 'data_inicio': self.data_inicio}

@dataclass(frozen=True)
class MedicaoAprovadaEvent(DomainEvent):
    obra_id: str = ''
    codigo_obra: str = ''
    medicao_id: str = ''
    valor_medido: str = '0.00'
    percentual_executado: str = '0.00'
    event_name: str = 'MedicaoAprovadaEvent'

    @classmethod
    def build(cls, *, obra_id: UUID, codigo_obra: str, medicao_id: UUID, valor_medido: Decimal, percentual_executado: Decimal) -> 'MedicaoAprovadaEvent':
        return cls(obra_id=str(obra_id), codigo_obra=codigo_obra, medicao_id=str(medicao_id), valor_medido=str(valor_medido), percentual_executado=str(percentual_executado))

    def to_payload(self) -> dict:
        return {**self._base_payload(), 'obra_id': self.obra_id, 'codigo_obra': self.codigo_obra, 'medicao_id': self.medicao_id, 'valor_medido': self.valor_medido, 'percentual_executado': self.percentual_executado}

@dataclass(frozen=True)
class AditivoAssinadoEvent(DomainEvent):
    obra_id: str = ''
    codigo_obra: str = ''
    aditivo_id: str = ''
    tipo: str = ''
    valor_adicional: str = '0.00'
    prazo_adicional_dias: int = 0
    event_name: str = 'AditivoAssinadoEvent'

    @classmethod
    def build(cls, *, obra_id: UUID, codigo_obra: str, aditivo_id: UUID, tipo: str, valor_adicional: Decimal, prazo_adicional_dias: int) -> 'AditivoAssinadoEvent':
        return cls(obra_id=str(obra_id), codigo_obra=codigo_obra, aditivo_id=str(aditivo_id), tipo=tipo, valor_adicional=str(valor_adicional), prazo_adicional_dias=prazo_adicional_dias)

    def to_payload(self) -> dict:
        return {**self._base_payload(), 'obra_id': self.obra_id, 'codigo_obra': self.codigo_obra, 'aditivo_id': self.aditivo_id, 'tipo': self.tipo, 'valor_adicional': self.valor_adicional, 'prazo_adicional_dias': self.prazo_adicional_dias}

@dataclass(frozen=True)
class ObraConcluidaEvent(DomainEvent):
    obra_id: str = ''
    codigo_obra: str = ''
    data_conclusao: str = ''
    event_name: str = 'ObraConcluidaEvent'

    @classmethod
    def build(cls, *, obra_id: UUID, codigo_obra: str, data_conclusao: datetime | str) -> 'ObraConcluidaEvent':
        data_conclusao_str = data_conclusao.isoformat() if hasattr(data_conclusao, 'isoformat') else str(data_conclusao)
        return cls(obra_id=str(obra_id), codigo_obra=codigo_obra, data_conclusao=data_conclusao_str)

    def to_payload(self) -> dict:
        return {**self._base_payload(), 'obra_id': self.obra_id, 'codigo_obra': self.codigo_obra, 'data_conclusao': self.data_conclusao}