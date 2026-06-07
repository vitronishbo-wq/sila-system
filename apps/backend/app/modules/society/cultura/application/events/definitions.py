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
        payload["timestamp"] = self.timestamp.isoformat()
        return payload


@dataclass(slots=True)
class ArtistaRegistradoEvent(DomainEvent):
    artista_id: UUID = field(default_factory=uuid4)
    nome: str = ""
    cpf: str = ""
    tipo: str = ""


@dataclass(slots=True)
class BemTombadoEvent(DomainEvent):
    bem_id: UUID = field(default_factory=uuid4)
    nome: str = ""
    tipo: str = ""
    nivel_tombamento: str = ""


@dataclass(slots=True)
class EventoProgramadoEvent(DomainEvent):
    evento_id: UUID = field(default_factory=uuid4)
    nome: str = ""
    tipo: str = ""
    data_inicio: str = ""
    data_fim: str = ""
    local: str = ""
    capacidade: int = 0


@dataclass(slots=True)
class ProjetoAprovadoEvent(DomainEvent):
    projeto_id: UUID = field(default_factory=uuid4)
    codigo_projeto: str = ""
    titulo: str = ""
    proponente: str = ""
    valor_aprovado: float = 0.0
    edital_id: UUID | None = None


@dataclass(slots=True)
class EditalPublicadoEvent(DomainEvent):
    edital_id: UUID = field(default_factory=uuid4)
    numero: str = ""
    titulo: str = ""
    tipo: str = ""
    valor_total: float = 0.0
    data_fim_inscricoes: str = ""
