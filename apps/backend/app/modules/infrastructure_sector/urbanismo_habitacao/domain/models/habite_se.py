from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusHabiteSe, TipoHabiteSe

@dataclass
class HabiteSe:
    id: UUID
    codigo_habite_se: str
    numero_processo: str
    tipo: TipoHabiteSe
    status: StatusHabiteSe
    alvara_id: UUID
    requerente_id: UUID
    provincia: str
    municipio: str | None = None
    endereco_imovel: str | None = None
    area_vistoriada: Decimal | None = None
    data_requerimento: date = field(default_factory=date.today)
    data_vistoria: date | None = None
    data_emissao: date | None = None
    data_validade: date | None = None
    tecnico_vistoriador_id: UUID | None = None
    observacoes: str | None = None
    data_atualizacao: date | None = None

    @classmethod
    def criar(cls, *, codigo_habite_se: str, numero_processo: str, tipo: TipoHabiteSe, alvara_id: UUID, requerente_id: UUID, provincia: str, municipio: str | None=None, endereco_imovel: str | None=None, area_vistoriada: Decimal | None=None) -> 'HabiteSe':
        if not codigo_habite_se.strip():
            raise ValueError('Codigo do habite-se e obrigatorio')
        if not numero_processo.strip():
            raise ValueError('Numero do processo e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia e obrigatoria')
        if area_vistoriada is not None and area_vistoriada <= 0:
            raise ValueError('Area vistoriada deve ser maior que zero')
        return cls(id=uuid4(), codigo_habite_se=codigo_habite_se.strip(), numero_processo=numero_processo.strip(), tipo=tipo, status=StatusHabiteSe.REQUERIDO, alvara_id=alvara_id, requerente_id=requerente_id, provincia=provincia.strip(), municipio=municipio.strip() if municipio else None, endereco_imovel=endereco_imovel.strip() if endereco_imovel else None, area_vistoriada=area_vistoriada)

    def agendar_vistoria(self, *, data_vistoria: date, tecnico_vistoriador_id: UUID) -> None:
        if self.status != StatusHabiteSe.REQUERIDO:
            raise ValueError('Habite-se precisa estar requerido')
        if data_vistoria < date.today():
            raise ValueError('Data da vistoria nao pode ser no passado')
        self.status = StatusHabiteSe.EM_VISTORIA
        self.data_vistoria = data_vistoria
        self.tecnico_vistoriador_id = tecnico_vistoriador_id
        self.data_atualizacao = date.today()

    def aprovar_vistoria(self) -> None:
        if self.status != StatusHabiteSe.EM_VISTORIA:
            raise ValueError('Habite-se precisa estar em vistoria')
        self.status = StatusHabiteSe.APROVADO
        self.data_atualizacao = date.today()

    def reprovar_vistoria(self, *, motivo: str) -> None:
        if self.status != StatusHabiteSe.EM_VISTORIA:
            raise ValueError('Habite-se precisa estar em vistoria')
        if not motivo.strip():
            raise ValueError('Motivo da reprovacao e obrigatorio')
        self.status = StatusHabiteSe.REPROVADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def emitir(self, *, data_emissao: date, data_validade: date | None=None) -> None:
        if self.status != StatusHabiteSe.APROVADO:
            raise ValueError('Habite-se precisa estar aprovado')
        if data_validade is not None and data_validade <= data_emissao:
            raise ValueError('Data de validade deve ser maior que data de emissao')
        self.status = StatusHabiteSe.EMITIDO
        self.data_emissao = data_emissao
        self.data_validade = data_validade
        self.data_atualizacao = date.today()

    def cancelar(self, *, motivo: str) -> None:
        if self.status in {StatusHabiteSe.CANCELADO, StatusHabiteSe.REPROVADO}:
            raise ValueError('Habite-se nao pode ser cancelado neste status')
        if not motivo.strip():
            raise ValueError('Motivo do cancelamento e obrigatorio')
        self.status = StatusHabiteSe.CANCELADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()