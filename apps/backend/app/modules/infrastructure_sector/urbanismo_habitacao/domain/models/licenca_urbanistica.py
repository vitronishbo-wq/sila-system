from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLicencaUrbanistica, TipoAlvara

@dataclass
class LicencaUrbanistica:
    id: UUID
    codigo_licenca: str
    numero_processo: str
    tipo_alvara: TipoAlvara
    status: StatusLicencaUrbanistica
    requerente_id: UUID
    zoneamento_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_obra: str | None = None
    area_construida_prevista: Decimal | None = None
    data_requerimento: date = field(default_factory=date.today)
    data_emissao: date | None = None
    data_validade: date | None = None
    tecnico_responsavel_id: UUID | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None

    @classmethod
    def criar(cls, *, codigo_licenca: str, numero_processo: str, tipo_alvara: TipoAlvara, requerente_id: UUID, zoneamento_id: UUID, provincia: str, municipio: str | None=None, endereco_obra: str | None=None, area_construida_prevista: Decimal | None=None) -> 'LicencaUrbanistica':
        if not codigo_licenca.strip():
            raise ValueError('Codigo da licenca e obrigatorio')
        if not numero_processo.strip():
            raise ValueError('Numero do processo e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia e obrigatoria')
        if area_construida_prevista is not None and area_construida_prevista <= 0:
            raise ValueError('Area construida prevista deve ser maior que zero')
        return cls(id=uuid4(), codigo_licenca=codigo_licenca.strip(), numero_processo=numero_processo.strip(), tipo_alvara=tipo_alvara, status=StatusLicencaUrbanistica.REQUERIDA, requerente_id=requerente_id, zoneamento_id=zoneamento_id, provincia=provincia.strip(), municipio=municipio.strip() if municipio else None, endereco_obra=endereco_obra.strip() if endereco_obra else None, area_construida_prevista=area_construida_prevista)

    def iniciar_analise(self) -> None:
        if self.status not in {StatusLicencaUrbanistica.REQUERIDA, StatusLicencaUrbanistica.PENDENTE_DOCUMENTACAO}:
            raise ValueError('Licenca precisa estar requerida ou pendente de documentacao')
        self.status = StatusLicencaUrbanistica.EM_ANALISE
        self.data_atualizacao = date.today()

    def solicitar_pendencia(self, *, motivo: str) -> None:
        if self.status != StatusLicencaUrbanistica.EM_ANALISE:
            raise ValueError('Licenca precisa estar em analise')
        if not motivo.strip():
            raise ValueError('Motivo da pendencia e obrigatorio')
        self.status = StatusLicencaUrbanistica.PENDENTE_DOCUMENTACAO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def deferir(self, *, data_emissao: date, data_validade: date, tecnico_responsavel_id: UUID) -> None:
        if self.status != StatusLicencaUrbanistica.EM_ANALISE:
            raise ValueError('Licenca precisa estar em analise')
        if data_validade <= data_emissao:
            raise ValueError('Data de validade deve ser maior que data de emissao')
        self.status = StatusLicencaUrbanistica.DEFERIDA
        self.data_emissao = data_emissao
        self.data_validade = data_validade
        self.tecnico_responsavel_id = tecnico_responsavel_id
        self.data_atualizacao = date.today()

    def indeferir(self, *, motivo: str) -> None:
        if self.status not in {StatusLicencaUrbanistica.EM_ANALISE, StatusLicencaUrbanistica.PENDENTE_DOCUMENTACAO}:
            raise ValueError('Licenca precisa estar em analise ou pendente')
        if not motivo.strip():
            raise ValueError('Motivo do indeferimento e obrigatorio')
        self.status = StatusLicencaUrbanistica.INDEFERIDA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def cancelar(self, *, motivo: str) -> None:
        if self.status in {StatusLicencaUrbanistica.CANCELADA, StatusLicencaUrbanistica.INDEFERIDA}:
            raise ValueError('Licenca nao pode ser cancelada neste status')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusLicencaUrbanistica.CANCELADA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()