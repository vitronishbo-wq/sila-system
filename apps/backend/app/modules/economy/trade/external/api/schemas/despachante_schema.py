from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.api.schemas.operador_logistico_schema import (
    CancelamentoOperadorInput,
    HabilitacaoOperadorInput,
    OperadorLogisticoCreate,
    OperadorLogisticoResponse,
    SuspensaoOperadorInput,
)


class DespachanteCreate(OperadorLogisticoCreate):
    pass


class HabilitacaoDespachanteInput(HabilitacaoOperadorInput):
    pass


class SuspensaoDespachanteInput(SuspensaoOperadorInput):
    pass


class CancelamentoDespachanteInput(CancelamentoOperadorInput):
    pass


class DespachanteResponse(OperadorLogisticoResponse):
    pass
