from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class DemandaOperacionalResponse(BaseModel):
    viagens_total: int
    passageiros_total: int
    passageiros_media_por_viagem: Decimal
    arrecadacao_total: Decimal


class QualidadeServicoResponse(BaseModel):
    viagens_total: int
    viagens_concluidas: int
    viagens_canceladas: int
    viagens_atrasadas: int
    pontualidade_percentual: Decimal
    taxa_cancelamento_percentual: Decimal
    taxa_atraso_percentual: Decimal
