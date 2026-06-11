from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from apps.backend.app.core.events.domain_event import DomainEvent as CoreDomainEvent


@dataclass(slots=True)
class ProcessDomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    def to_payload(self) -> dict:
        payload = asdict(self)
        payload["timestamp"] = self.timestamp.isoformat()
        return payload

    def to_domain_event(
        self,
        aggregate_type: str,
        aggregate_id: UUID,
        correlation_id: UUID | None = None,
        causation_id: UUID | None = None,
    ) -> CoreDomainEvent:
        """Convert the lightweight process contract into a Core DomainEvent instance."""
        return CoreDomainEvent(
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            event_type=self.__class__.__name__,
            timestamp=self.timestamp,
            version=self.version,
            event_id=self.event_id,
            metadata=self.to_payload(),
            correlation_id=correlation_id,
            causation_id=causation_id,
        )


# ------------------------
# Licenciamento Comercial
# ------------------------


@dataclass(slots=True)
class PedidoSubmetidoEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    empresa_id: UUID | None = None
    dados: dict = field(default_factory=dict)


@dataclass(slots=True)
class ValidacaoFiscalConcluidaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    valid: bool = False
    details: dict = field(default_factory=dict)


@dataclass(slots=True)
class ValidacaoLocalConcluidaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    valid: bool = False
    inspector: str | None = None


@dataclass(slots=True)
class LicencaEmitidaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    licenca_id: UUID = field(default_factory=uuid4)
    referencia: str | None = None


# -----------------
# Benefício Social
# -----------------


@dataclass(slots=True)
class PedidoBeneficioEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    beneficiario_id: UUID | None = None
    dados: dict = field(default_factory=dict)


@dataclass(slots=True)
class VerificacaoNifConcluidaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    nif: str | None = None
    valid: bool = False


@dataclass(slots=True)
class VerificacaoSSConcluidaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    ss_number: str | None = None
    valid: bool = False


@dataclass(slots=True)
class BeneficioAprovadoEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    beneficio_id: UUID = field(default_factory=uuid4)
    valor: float = 0.0


# ---------------------
# Contratação Pública
# ---------------------


@dataclass(slots=True)
class ConcursoPublicadoEvent(ProcessDomainEvent):
    concurso_id: UUID = field(default_factory=uuid4)
    titulo: str | None = None


@dataclass(slots=True)
class PropostaSubmetidaEvent(ProcessDomainEvent):
    proposta_id: UUID = field(default_factory=uuid4)
    concurso_id: UUID = field(default_factory=uuid4)
    fornecedor_id: UUID | None = None


@dataclass(slots=True)
class AvaliacaoConcluidaEvent(ProcessDomainEvent):
    concurso_id: UUID = field(default_factory=uuid4)
    avaliador: str | None = None
    resultado: dict = field(default_factory=dict)


@dataclass(slots=True)
class AdjudicacaoEmitidaEvent(ProcessDomainEvent):
    concurso_id: UUID = field(default_factory=uuid4)
    adjudicacao_id: UUID = field(default_factory=uuid4)
    vencedor_id: UUID | None = None


# ---------------------
# Transferência Escolar
# ---------------------


@dataclass(slots=True)
class PedidoTransferenciaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    aluno_id: UUID | None = None
    escola_origem_id: UUID | None = None
    escola_destino_id: UUID | None = None


@dataclass(slots=True)
class ValidacaoEscolaOrigemEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    escola_id: UUID | None = None
    valid: bool = False


@dataclass(slots=True)
class ValidacaoEscolaDestinoEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    escola_id: UUID | None = None
    valid: bool = False


@dataclass(slots=True)
class MatriculaTransferidaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    matricula_id: UUID = field(default_factory=uuid4)


# -------------
# Aposentação
# -------------


@dataclass(slots=True)
class PedidoAposentacaoEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    requerente_id: UUID | None = None


@dataclass(slots=True)
class TempoServicoValidadoEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    meses_validos: int = 0


@dataclass(slots=True)
class BeneficioCalculadoEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    valor_estimado: float = 0.0


@dataclass(slots=True)
class AposentacaoConcedidaEvent(ProcessDomainEvent):
    pedido_id: UUID = field(default_factory=uuid4)
    beneficio_id: UUID = field(default_factory=uuid4)


# -----------------
# Nascimento (NASCIMENTO_BI_NIF_SS)
# -----------------

@dataclass(slots=True)
class RegistoNascimentoCriadoEvent(ProcessDomainEvent):
    registro_id: UUID = field(default_factory=uuid4)
    dados: dict = field(default_factory=dict)


@dataclass(slots=True)
class CertidaoEmitidaEvent(ProcessDomainEvent):
    registro_id: UUID = field(default_factory=uuid4)
    certidao_id: UUID = field(default_factory=uuid4)
    referencia: str | None = None
    valid: bool = True


@dataclass(slots=True)
class NIFAtribuidoEvent(ProcessDomainEvent):
    registro_id: UUID = field(default_factory=uuid4)
    nif: str | None = None


@dataclass(slots=True)
class SSAtribuidoEvent(ProcessDomainEvent):
    registro_id: UUID = field(default_factory=uuid4)
    ss_number: str | None = None


@dataclass(slots=True)
class RegistroCanceladoEvent(ProcessDomainEvent):
    registro_id: UUID = field(default_factory=uuid4)
    motivo: str | None = None


__all__ = [
    "ProcessDomainEvent",
    # Licenciamento Comercial
    "PedidoSubmetidoEvent",
    "ValidacaoFiscalConcluidaEvent",
    "ValidacaoLocalConcluidaEvent",
    "LicencaEmitidaEvent",
    # Beneficio Social
    "PedidoBeneficioEvent",
    "VerificacaoNifConcluidaEvent",
    "VerificacaoSSConcluidaEvent",
    "BeneficioAprovadoEvent",
    # Contratacao Publica
    "ConcursoPublicadoEvent",
    "PropostaSubmetidaEvent",
    "AvaliacaoConcluidaEvent",
    "AdjudicacaoEmitidaEvent",
    # Transferencia Escolar
    "PedidoTransferenciaEvent",
    "ValidacaoEscolaOrigemEvent",
    "ValidacaoEscolaDestinoEvent",
    "MatriculaTransferidaEvent",
    # Aposentacao
    "PedidoAposentacaoEvent",
    "TempoServicoValidadoEvent",
    "BeneficioCalculadoEvent",
    "AposentacaoConcedidaEvent",
    # Nascimento
    "RegistoNascimentoCriadoEvent",
    "CertidaoEmitidaEvent",
    "NIFAtribuidoEvent",
    "SSAtribuidoEvent",
    "RegistroCanceladoEvent",
]
