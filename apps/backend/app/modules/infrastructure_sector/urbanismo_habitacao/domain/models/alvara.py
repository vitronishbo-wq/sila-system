from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusAlvara, TipoAlvara

@dataclass
class Alvara:
    id: UUID
    codigo_alvara: str
    numero_processo: str
    tipo: TipoAlvara
    status: StatusAlvara
    licenca_urbanistica_id: UUID
    requerente_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_obra: str | None = None
    area_autorizada: Decimal | None = None
    data_requerimento: date = field(default_factory=date.today)
    data_emissao: date | None = None
    data_validade: date | None = None
    analista_id: UUID | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None

    @classmethod
    def criar(cls, *, codigo_alvara: str, numero_processo: str, tipo: TipoAlvara, licenca_urbanistica_id: UUID, requerente_id: UUID, provincia: str, municipio: str | None=None, endereco_obra: str | None=None, area_autorizada: Decimal | None=None) -> 'Alvara':
        if not codigo_alvara.strip():
            raise ValueError('Codigo do alvara e obrigatorio')
        if not numero_processo.strip():
            raise ValueError('Numero do processo e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia e obrigatoria')
        if area_autorizada is not None and area_autorizada <= 0:
            raise ValueError('Area autorizada deve ser maior que zero')
        return cls(id=uuid4(), codigo_alvara=codigo_alvara.strip(), numero_processo=numero_processo.strip(), tipo=tipo, status=StatusAlvara.REQUERIDO, licenca_urbanistica_id=licenca_urbanistica_id, requerente_id=requerente_id, provincia=provincia.strip(), municipio=municipio.strip() if municipio else None, endereco_obra=endereco_obra.strip() if endereco_obra else None, area_autorizada=area_autorizada)

    def iniciar_analise(self) -> None:
        if self.status not in {StatusAlvara.REQUERIDO, StatusAlvara.PENDENCIA}:
            raise ValueError('Alvara precisa estar requerido ou em pendencia')
        self.status = StatusAlvara.EM_ANALISE
        self.data_atualizacao = date.today()

    def solicitar_pendencia(self, *, motivo: str) -> None:
        if self.status != StatusAlvara.EM_ANALISE:
            raise ValueError('Alvara precisa estar em analise')
        if not motivo.strip():
            raise ValueError('Motivo da pendencia e obrigatorio')
        self.status = StatusAlvara.PENDENCIA
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def deferir(self, *, data_emissao: date, data_validade: date, analista_id: UUID) -> None:
        if self.status != StatusAlvara.EM_ANALISE:
            raise ValueError('Alvara precisa estar em analise')
        if data_validade <= data_emissao:
            raise ValueError('Data de validade deve ser maior que data de emissao')
        self.status = StatusAlvara.DEFERIDO
        self.data_emissao = data_emissao
        self.data_validade = data_validade
        self.analista_id = analista_id
        self.data_atualizacao = date.today()

    def indeferir(self, *, motivo: str) -> None:
        if self.status not in {StatusAlvara.EM_ANALISE, StatusAlvara.PENDENCIA}:
            raise ValueError('Alvara precisa estar em analise ou pendencia')
        if not motivo.strip():
            raise ValueError('Motivo do indeferimento e obrigatorio')
        self.status = StatusAlvara.INDEFERIDO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def cancelar(self, *, motivo: str) -> None:
        if self.status in {StatusAlvara.CANCELADO, StatusAlvara.INDEFERIDO}:
            raise ValueError('Alvara nao pode ser cancelado neste status')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusAlvara.CANCELADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()