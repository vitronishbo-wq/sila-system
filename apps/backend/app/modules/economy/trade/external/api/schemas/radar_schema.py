from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.schemas.operador_logistico_schema import CancelamentoOperadorInput, HabilitacaoOperadorInput, OperadorLogisticoCreate, OperadorLogisticoResponse, SuspensaoOperadorInput

class RadarCreate(OperadorLogisticoCreate):
    pass

class HabilitacaoRadarInput(HabilitacaoOperadorInput):
    pass

class SuspensaoRadarInput(SuspensaoOperadorInput):
    pass

class CancelamentoRadarInput(CancelamentoOperadorInput):
    pass

class RadarResponse(OperadorLogisticoResponse):
    pass