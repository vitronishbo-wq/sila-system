from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4
from app.modules.resources.aguas_saneamento.domain.enums import StatusInfraestrutura, TipoInfraestrutura

@dataclass
class InfraestruturaHidrica:
    id: UUID
    codigo_infraestrutura: str
    tipo: TipoInfraestrutura
    nome: str
    provincia: str
    municipio: str
    status: StatusInfraestrutura
    data_registro: date
    capacidade: Decimal | None = None
    unidade_capacidade: str | None = None
    outorga_id: UUID | None = None
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    data_operacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(cls, *, tipo: TipoInfraestrutura, nome: str, provincia: str, municipio: str, capacidade: Decimal | None=None, unidade_capacidade: str | None=None, outorga_id: UUID | None=None, latitude: Decimal | None=None, longitude: Decimal | None=None) -> 'InfraestruturaHidrica':
        if not nome.strip():
            raise ValueError('Nome da infraestrutura e obrigatorio')
        if not provincia.strip():
            raise ValueError('Provincia da infraestrutura e obrigatoria')
        if not municipio.strip():
            raise ValueError('Municipio da infraestrutura e obrigatorio')
        if capacidade is not None and capacidade <= Decimal('0'):
            raise ValueError('Capacidade deve ser maior que zero')
        if capacidade is not None and (unidade_capacidade is None or not unidade_capacidade.strip()):
            raise ValueError('Unidade da capacidade e obrigatoria quando capacidade for informada')
        return cls(id=uuid4(), codigo_infraestrutura='', tipo=tipo, nome=nome.strip(), provincia=provincia.strip(), municipio=municipio.strip(), status=StatusInfraestrutura.PLANEJADA, data_registro=date.today(), capacidade=capacidade.quantize(Decimal('0.01')) if capacidade is not None else None, unidade_capacidade=unidade_capacidade.strip() if unidade_capacidade else None, outorga_id=outorga_id, latitude=latitude, longitude=longitude)

    def ativar(self, *, data_operacao: date | None=None) -> None:
        if self.status not in {StatusInfraestrutura.PLANEJADA, StatusInfraestrutura.MANUTENCAO, StatusInfraestrutura.INTERDITADA, StatusInfraestrutura.INATIVA}:
            raise ValueError('Infraestrutura nao pode ser ativada neste status')
        self.status = StatusInfraestrutura.OPERACIONAL
        self.data_operacao = data_operacao or date.today()
        self.observacoes = None

    def colocar_em_manutencao(self, motivo: str) -> None:
        if self.status != StatusInfraestrutura.OPERACIONAL:
            raise ValueError('Apenas infraestrutura operacional pode entrar em manutencao')
        if not motivo.strip():
            raise ValueError('Motivo da manutencao e obrigatorio')
        self.status = StatusInfraestrutura.MANUTENCAO
        self.observacoes = motivo.strip()

    def interditar(self, motivo: str) -> None:
        if self.status == StatusInfraestrutura.INTERDITADA:
            raise ValueError('Infraestrutura ja interditada')
        if self.status == StatusInfraestrutura.INATIVA:
            raise ValueError('Infraestrutura inativa nao pode ser interditada')
        if not motivo.strip():
            raise ValueError('Motivo da interdicao e obrigatorio')
        self.status = StatusInfraestrutura.INTERDITADA
        self.observacoes = motivo.strip()

    def reativar(self, motivo: str | None=None) -> None:
        if self.status not in {StatusInfraestrutura.MANUTENCAO, StatusInfraestrutura.INTERDITADA}:
            raise ValueError('Apenas infraestrutura em manutencao/interditada pode ser reativada')
        self.status = StatusInfraestrutura.OPERACIONAL
        self.observacoes = motivo.strip() if motivo else None

    def desativar(self, motivo: str) -> None:
        if self.status == StatusInfraestrutura.INATIVA:
            raise ValueError('Infraestrutura ja inativa')
        if not motivo.strip():
            raise ValueError('Motivo da desativacao e obrigatorio')
        self.status = StatusInfraestrutura.INATIVA
        self.observacoes = motivo.strip()