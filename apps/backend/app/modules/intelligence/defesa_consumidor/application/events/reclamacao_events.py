from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ReclamacaoCriadaEvent:
    id: int
    protocolo: str
    consumidor_id: int
    estabelecimento_id: int
    categoria: str
    valor_reclamado: float | None
    data_abertura: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class ReclamacaoStatusAtualizadoEvent:
    id: int
    protocolo: str
    status_anterior: str
    status_novo: str
    data_atualizacao: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class ReclamacaoFinalizadaEvent:
    id: int
    protocolo: str
    resolvido: bool
    data_resolucao: str
    tempo_resolucao_dias: int
    descricao_resposta: str | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class ReclamacaoPrioridadeEscaladaEvent:
    id: int
    protocolo: str
    prioridade_anterior: str
    prioridade_nova: str
    motivo_escalonamento: str | None = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


DEFESA_CONSUMIDOR_EVENTS = [
    ReclamacaoCriadaEvent,
    ReclamacaoStatusAtualizadoEvent,
    ReclamacaoFinalizadaEvent,
    ReclamacaoPrioridadeEscaladaEvent,
]
