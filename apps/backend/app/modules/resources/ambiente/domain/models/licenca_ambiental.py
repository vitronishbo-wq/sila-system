from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.ambiente.domain.enums import StatusLicenca, TipoLicenca


@dataclass
class LicencaAmbiental:
    id: UUID
    numero_licenca: str
    numero_car: str
    tipo: TipoLicenca
    atividade: str
    status: StatusLicenca
    data_requerimento: date
    data_analise: date | None = None
    data_emissao: date | None = None
    data_validade: date | None = None
    analista_id: UUID | None = None
    condicionantes: list[str] | None = None
    observacoes: str | None = None

    @classmethod
    def criar(cls, *, numero_car: str, tipo: TipoLicenca, atividade: str) -> LicencaAmbiental:
        if not atividade.strip():
            raise ValueError("Atividade e obrigatoria")
        return cls(
            id=uuid4(),
            numero_licenca="",
            numero_car=numero_car,
            tipo=tipo,
            atividade=atividade.strip(),
            status=StatusLicenca.REQUERIDA,
            data_requerimento=date.today(),
            condicionantes=[],
        )

    def iniciar_analise(self) -> None:
        if self.status != StatusLicenca.REQUERIDA:
            raise ValueError("Apenas licenca requerida pode entrar em analise")
        self.status = StatusLicenca.EM_ANALISE
        self.data_analise = date.today()

    def deferir(
        self, *, analista_id: UUID, data_validade: date, condicionantes: list[str] | None = None
    ) -> None:
        if self.status != StatusLicenca.EM_ANALISE:
            raise ValueError("Licenca precisa estar em analise para deferimento")
        if data_validade <= date.today():
            raise ValueError("Data de validade deve ser futura")
        self.status = StatusLicenca.DEFERIDA
        self.analista_id = analista_id
        self.data_emissao = date.today()
        self.data_validade = data_validade
        self.condicionantes = condicionantes or []
        self.observacoes = None

    def indeferir(self, *, analista_id: UUID, motivo: str) -> None:
        if self.status != StatusLicenca.EM_ANALISE:
            raise ValueError("Licenca precisa estar em analise para indeferimento")
        if not motivo.strip():
            raise ValueError("Motivo do indeferimento e obrigatorio")
        self.status = StatusLicenca.INDEFERIDA
        self.analista_id = analista_id
        self.observacoes = motivo.strip()

    def suspender(self, *, motivo: str) -> None:
        if self.status != StatusLicenca.DEFERIDA:
            raise ValueError("Apenas licenca deferida pode ser suspensa")
        if not motivo.strip():
            raise ValueError("Motivo da suspensao e obrigatorio")
        self.status = StatusLicenca.SUSPENSA
        self.observacoes = motivo.strip()

    def cancelar(self, *, motivo: str) -> None:
        if self.status in {StatusLicenca.CANCELADA, StatusLicenca.VENCIDA}:
            raise ValueError("Licenca ja encerrada")
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        self.status = StatusLicenca.CANCELADA
        self.observacoes = motivo.strip()
