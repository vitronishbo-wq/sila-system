from __future__ import annotations
from app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class DrawbackSubstituicaoCreate(HabilitacaoCreateBase):
    pass

class DrawbackSubstituicaoAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class DrawbackSubstituicaoRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class DrawbackSubstituicaoResponse(HabilitacaoResponseBase):
    pass