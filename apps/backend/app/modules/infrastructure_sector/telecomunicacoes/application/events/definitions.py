from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.telecomunicacoes.domain.models.fatura_telecom import FaturaTelecom
from app.modules.infrastructure_sector.telecomunicacoes.domain.models.reclamacao import Reclamacao

@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID
    timestamp: datetime
    version: int = field(default=1, init=False)

    @staticmethod
    def now() -> datetime:
        return datetime.now(timezone.utc)

@dataclass(frozen=True)
class FaturaTelecomGeradaEvent(DomainEvent):
    fatura_id: UUID
    numero_fatura: str
    assinante_id: UUID
    referencia: str
    valor_total: Decimal
    event_name = 'FaturaTelecomGeradaEvent'

    @classmethod
    def from_fatura(cls, fatura: FaturaTelecom) -> 'FaturaTelecomGeradaEvent':
        return cls(event_id=uuid4(), timestamp=DomainEvent.now(), fatura_id=fatura.id, numero_fatura=fatura.numero_fatura, assinante_id=fatura.assinante_id, referencia=fatura.referencia, valor_total=fatura.valor_total)

    def to_payload(self) -> dict:
        return {'event_id': str(self.event_id), 'timestamp': self.timestamp.isoformat(), 'version': self.version, 'fatura_id': str(self.fatura_id), 'numero_fatura': self.numero_fatura, 'assinante_id': str(self.assinante_id), 'referencia': self.referencia, 'valor_total': str(self.valor_total)}

    @classmethod
    def from_payload(cls, payload: dict) -> 'FaturaTelecomGeradaEvent':
        return cls(event_id=UUID(payload['event_id']), timestamp=datetime.fromisoformat(payload['timestamp']), fatura_id=UUID(payload['fatura_id']), numero_fatura=payload['numero_fatura'], assinante_id=UUID(payload['assinante_id']), referencia=payload['referencia'], valor_total=Decimal(payload['valor_total']))

@dataclass(frozen=True)
class ReclamacaoTelecomAbertaEvent(DomainEvent):
    reclamacao_id: UUID
    protocolo: str
    assinante_id: UUID
    tipo: str
    prioridade: str
    event_name = 'ReclamacaoTelecomAbertaEvent'

    @classmethod
    def from_reclamacao(cls, reclamacao: Reclamacao) -> 'ReclamacaoTelecomAbertaEvent':
        return cls(event_id=uuid4(), timestamp=DomainEvent.now(), reclamacao_id=reclamacao.id, protocolo=reclamacao.protocolo, assinante_id=reclamacao.assinante_id, tipo=reclamacao.tipo.value, prioridade=reclamacao.prioridade)

    def to_payload(self) -> dict:
        return {'event_id': str(self.event_id), 'timestamp': self.timestamp.isoformat(), 'version': self.version, 'reclamacao_id': str(self.reclamacao_id), 'protocolo': self.protocolo, 'assinante_id': str(self.assinante_id), 'tipo': self.tipo, 'prioridade': self.prioridade}

    @classmethod
    def from_payload(cls, payload: dict) -> 'ReclamacaoTelecomAbertaEvent':
        return cls(event_id=UUID(payload['event_id']), timestamp=datetime.fromisoformat(payload['timestamp']), reclamacao_id=UUID(payload['reclamacao_id']), protocolo=payload['protocolo'], assinante_id=UUID(payload['assinante_id']), tipo=payload['tipo'], prioridade=payload['prioridade'])

@dataclass(frozen=True)
class QualidadeServicoAferidaEvent(DomainEvent):
    assinante_id: UUID
    referencia: str
    download_mbps: Decimal
    upload_mbps: Decimal
    latencia_ms: Decimal
    conforme: bool
    event_name = 'QualidadeServicoAferidaEvent'

    def to_payload(self) -> dict:
        return {'event_id': str(self.event_id), 'timestamp': self.timestamp.isoformat(), 'version': self.version, 'assinante_id': str(self.assinante_id), 'referencia': self.referencia, 'download_mbps': str(self.download_mbps), 'upload_mbps': str(self.upload_mbps), 'latencia_ms': str(self.latencia_ms), 'conforme': self.conforme}

    @classmethod
    def from_payload(cls, payload: dict) -> 'QualidadeServicoAferidaEvent':
        return cls(event_id=UUID(payload['event_id']), timestamp=datetime.fromisoformat(payload['timestamp']), assinante_id=UUID(payload['assinante_id']), referencia=payload['referencia'], download_mbps=Decimal(payload['download_mbps']), upload_mbps=Decimal(payload['upload_mbps']), latencia_ms=Decimal(payload['latencia_ms']), conforme=bool(payload['conforme']))