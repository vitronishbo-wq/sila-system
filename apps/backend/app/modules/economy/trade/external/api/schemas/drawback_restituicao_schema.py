from __future__ import annotations
from app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class DrawbackRestituicaoCreate(HabilitacaoCreateBase):
    pass

class DrawbackRestituicaoAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class DrawbackRestituicaoRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class DrawbackRestituicaoResponse(HabilitacaoResponseBase):
    pass