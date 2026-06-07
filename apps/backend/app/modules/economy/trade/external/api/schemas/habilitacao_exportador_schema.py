from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.api.schemas.habilitacao_schema_base import (
    HabilitacaoAprovacaoInput,
    HabilitacaoCreateBase,
    HabilitacaoRejeicaoInput,
    HabilitacaoResponseBase,
)


class HabilitacaoExportadorCreate(HabilitacaoCreateBase):
    pass


class HabilitacaoExportadorAprovacaoInput(HabilitacaoAprovacaoInput):
    pass


class HabilitacaoExportadorRejeicaoInput(HabilitacaoRejeicaoInput):
    pass


class HabilitacaoExportadorResponse(HabilitacaoResponseBase):
    pass
