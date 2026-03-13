from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.schemas.operador_logistico_schema import CancelamentoOperadorInput, HabilitacaoOperadorInput, OperadorLogisticoCreate, OperadorLogisticoResponse, SuspensaoOperadorInput

class TransportadorInternacionalCreate(OperadorLogisticoCreate):
    pass

class HabilitacaoTransportadorInternacionalInput(HabilitacaoOperadorInput):
    pass

class SuspensaoTransportadorInternacionalInput(SuspensaoOperadorInput):
    pass

class CancelamentoTransportadorInternacionalInput(CancelamentoOperadorInput):
    pass

class TransportadorInternacionalResponse(OperadorLogisticoResponse):
    pass