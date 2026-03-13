from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import HabilitacaoAprovacaoInput, HabilitacaoCreateBase, HabilitacaoRejeicaoInput, HabilitacaoResponseBase

class SiscomexDrawbackCreate(HabilitacaoCreateBase):
    pass

class SiscomexDrawbackAprovacaoInput(HabilitacaoAprovacaoInput):
    pass

class SiscomexDrawbackRejeicaoInput(HabilitacaoRejeicaoInput):
    pass

class SiscomexDrawbackResponse(HabilitacaoResponseBase):
    pass