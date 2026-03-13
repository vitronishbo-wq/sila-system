from __future__ import annotations
from app.modules.economy.trade.external.application.ports.operador_logistico_repository_port import OperadorLogisticoRepositoryPort
from app.modules.economy.trade.external.domain.models import AgenteCarga

class AgenteCargaRepositoryPort(OperadorLogisticoRepositoryPort[AgenteCarga]):
    pass