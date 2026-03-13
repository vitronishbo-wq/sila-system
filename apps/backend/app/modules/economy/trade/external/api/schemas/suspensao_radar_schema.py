from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class SuspensaoRadarCreate(HabilitacaoCreateBase):
    pass

class SuspensaoRadarAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class SuspensaoRadarRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class SuspensaoRadarResponse(HabilitacaoResponseBase):
    pass