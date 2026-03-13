from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class DrawbackExternoCreate(HabilitacaoCreateBase):
    pass

class DrawbackExternoAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class DrawbackExternoRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class DrawbackExternoResponse(HabilitacaoResponseBase):
    pass