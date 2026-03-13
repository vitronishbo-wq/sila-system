from __future__ import annotations
from apps.backend.app.modules.economy.trade.external.api.schemas.operador_logistico_schema import CancelamentoOperadorInput, HabilitacaoOperadorInput, OperadorLogisticoCreate, OperadorLogisticoResponse, SuspensaoOperadorInput

class AgenteCargaCreate(OperadorLogisticoCreate):
    pass

class HabilitacaoAgenteCargaInput(HabilitacaoOperadorInput):
    pass

class SuspensaoAgenteCargaInput(SuspensaoOperadorInput):
    pass

class CancelamentoAgenteCargaInput(CancelamentoOperadorInput):
    pass

class AgenteCargaResponse(OperadorLogisticoResponse):
    pass