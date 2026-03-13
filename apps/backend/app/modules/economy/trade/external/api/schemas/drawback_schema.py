from __future__ import annotations
from app.modules.economy.trade.external.api.schemas.operador_logistico_schema import CancelamentoOperadorInput, HabilitacaoOperadorInput, OperadorLogisticoCreate, OperadorLogisticoResponse, SuspensaoOperadorInput

class DrawbackCreate(OperadorLogisticoCreate):
    pass

class HabilitacaoDrawbackInput(HabilitacaoOperadorInput):
    pass

class SuspensaoDrawbackInput(SuspensaoOperadorInput):
    pass

class CancelamentoDrawbackInput(CancelamentoOperadorInput):
    pass

class DrawbackResponse(OperadorLogisticoResponse):
    pass