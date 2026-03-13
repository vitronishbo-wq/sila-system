from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
from app.modules.resources.florestas.domain.enums import TipoCicloCorte, TipoManejo

@dataclass
class UnidadeManejo:
    id: UUID
    codigo_um: str
    nome: str
    area_total_ha: Decimal
    area_manejo_ha: Decimal
    area_preservacao_ha: Decimal
    tipo_manejo: TipoManejo
    ciclo_corte: TipoCicloCorte
    operador_id: UUID
    imovel_id: UUID
    plano_manejo_id: Optional[UUID] = None
    licenca_id: Optional[UUID] = None
    data_criacao: date = date.today()
    data_aprovacao: Optional[date] = None
    data_validade: Optional[date] = None
    coordenadas_centroide: Optional[str] = None
    arquivo_shp: Optional[str] = None
    observacoes: Optional[str] = None

    @classmethod
    def cadastrar(cls, *, nome: str, area_total_ha: Decimal, tipo_manejo: TipoManejo, ciclo_corte: TipoCicloCorte, operador_id: UUID, imovel_id: UUID, codigo_um: str) -> 'UnidadeManejo':
        return cls(id=uuid4(), codigo_um=codigo_um, nome=nome, area_total_ha=area_total_ha, area_manejo_ha=area_total_ha * Decimal('0.8'), area_preservacao_ha=area_total_ha * Decimal('0.2'), tipo_manejo=tipo_manejo, ciclo_corte=ciclo_corte, operador_id=operador_id, imovel_id=imovel_id, data_criacao=date.today())

    def aprovar_plano(self, *, plano_manejo_id: UUID, data_aprovacao: date, data_validade: date) -> None:
        self.plano_manejo_id = plano_manejo_id
        self.data_aprovacao = data_aprovacao
        self.data_validade = data_validade