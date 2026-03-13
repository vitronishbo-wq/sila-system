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
class AcordoAssinadoEvent(DomainEvent):
    acordo_id: UUID = field(default_factory=uuid4)
    numero_registro: str = ''
    titulo: str = ''
    tipo: str = ''
    partes: list[str] = field(default_factory=list)

@dataclass(slots=True)
class AcordoRatificadoEvent(DomainEvent):
    acordo_id: UUID = field(default_factory=uuid4)
    numero_registro: str = ''
    instrumento_ratificacao: str = ''

@dataclass(slots=True)
class AcordoVigorEvent(DomainEvent):
    acordo_id: UUID = field(default_factory=uuid4)
    numero_registro: str = ''
    prazo_anos: int | None = None

@dataclass(slots=True)
class ProjetoCooperacaoAprovadoEvent(DomainEvent):
    projeto_id: UUID = field(default_factory=uuid4)
    codigo_projeto: str = ''
    titulo: str = ''
    pais_parceiro_id: UUID = field(default_factory=uuid4)
    orcamento_total: float = 0.0

@dataclass(slots=True)
class VistoAprovadoEvent(DomainEvent):
    visto_id: UUID = field(default_factory=uuid4)
    numero_processo: str = ''
    solicitante_cpf: str = ''
    tipo: str = ''
    data_validade: str = ''