from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class DrawbackIsencaoCreate(HabilitacaoCreateBase):
    pass

class DrawbackIsencaoAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class DrawbackIsencaoRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class DrawbackIsencaoResponse(HabilitacaoResponseBase):
    pass