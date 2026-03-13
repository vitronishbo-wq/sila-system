from __future__ import annotations
from app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class DrawbackInternoCreate(HabilitacaoCreateBase):
    pass

class DrawbackInternoAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class DrawbackInternoRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class DrawbackInternoResponse(HabilitacaoResponseBase):
    pass