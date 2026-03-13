from __future__ import annotations
from app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class DrawbackSuspensaoCreate(HabilitacaoCreateBase):
    pass

class DrawbackSuspensaoAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class DrawbackSuspensaoRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class DrawbackSuspensaoResponse(HabilitacaoResponseBase):
    pass