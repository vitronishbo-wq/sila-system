from __future__ import annotations
from app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class DrawbackIntegradoCreate(HabilitacaoCreateBase):
    pass

class DrawbackIntegradoAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class DrawbackIntegradoRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class DrawbackIntegradoResponse(HabilitacaoResponseBase):
    pass