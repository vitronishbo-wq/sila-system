from __future__ import annotations
from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass(slots=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    def to_payload(self) -> dict:
        payload = asdict(self)
        payload['timestamp'] = self.timestamp.isoformat()
        return payload

@dataclass(slots=True)
class JogoAgendadoEvent(DomainEvent):
    jogo_id: UUID = field(default_factory=uuid4)
    codigo_jogo: str = ''
    competicao_id: UUID = field(default_factory=uuid4)
    clube_casa_id: UUID = field(default_factory=uuid4)
    clube_fora_id: UUID = field(default_factory=uuid4)
    data_jogo: str = ''

@dataclass(slots=True)
class JogoResultadoRegistradoEvent(DomainEvent):
    jogo_id: UUID = field(default_factory=uuid4)
    codigo_jogo: str = ''
    placar_casa: int = 0
    placar_fora: int = 0
    status: str = ''

@dataclass(slots=True)
class EstadioCadastradoEvent(DomainEvent):
    estadio_id: UUID = field(default_factory=uuid4)
    codigo_estadio: str = ''
    nome: str = ''
    municipio: str = ''
    provincia: str = ''

@dataclass(slots=True)
class TransferenciaSolicitadaEvent(DomainEvent):
    transferencia_id: UUID = field(default_factory=uuid4)
    codigo_transferencia: str = ''
    atleta_id: UUID = field(default_factory=uuid4)
    clube_origem_id: UUID = field(default_factory=uuid4)
    clube_destino_id: UUID = field(default_factory=uuid4)
    valor_transferencia: str | None = None
    status: str = ''

@dataclass(slots=True)
class TransferenciaConcluidaEvent(DomainEvent):
    transferencia_id: UUID = field(default_factory=uuid4)
    codigo_transferencia: str = ''
    atleta_id: UUID = field(default_factory=uuid4)
    clube_destino_id: UUID = field(default_factory=uuid4)
    data_conclusao: str = ''
    status: str = ''

@dataclass(slots=True)
class ContratoAssinadoEvent(DomainEvent):
    contrato_id: UUID = field(default_factory=uuid4)
    codigo_contrato: str = ''
    atleta_id: UUID = field(default_factory=uuid4)
    clube_id: UUID = field(default_factory=uuid4)
    tipo_contrato: str = ''
    data_inicio: str = ''
    data_fim: str = ''
    status: str = ''