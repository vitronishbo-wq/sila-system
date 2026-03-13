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
class AeronaveRegistradaEvent(DomainEvent):
    aeronave_id: UUID = field(default_factory=uuid4)
    matricula: str = ''
    modelo: str = ''
    proprietario_cpf_cnpj: str = ''

@dataclass(slots=True)
class VooProgramadoEvent(DomainEvent):
    voo_id: UUID = field(default_factory=uuid4)
    numero_voo: str = ''
    empresa_id: UUID = field(default_factory=uuid4)
    aeronave_id: UUID = field(default_factory=uuid4)
    origem: UUID = field(default_factory=uuid4)
    destino: UUID = field(default_factory=uuid4)
    partida_programada: datetime = field(default_factory=datetime.utcnow)

@dataclass(slots=True)
class VooDecoladoEvent(DomainEvent):
    voo_id: UUID = field(default_factory=uuid4)
    numero_voo: str = ''
    data_hora: datetime = field(default_factory=datetime.utcnow)
    atraso_minutos: int = 0

@dataclass(slots=True)
class VooPousadoEvent(DomainEvent):
    voo_id: UUID = field(default_factory=uuid4)
    numero_voo: str = ''
    data_hora: datetime = field(default_factory=datetime.utcnow)
    tempo_voo_horas: float = 0.0

@dataclass(slots=True)
class OcorrenciaRegistradaEvent(DomainEvent):
    ocorrencia_id: UUID = field(default_factory=uuid4)
    numero_ocorrencia: str = ''
    tipo: str = ''
    aeronave_id: UUID = field(default_factory=uuid4)
    gravidade: str = ''
    data_ocorrencia: datetime = field(default_factory=datetime.utcnow)