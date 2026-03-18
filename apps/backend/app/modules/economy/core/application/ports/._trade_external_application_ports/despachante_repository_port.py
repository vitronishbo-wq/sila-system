from __future__ import annotations
from ....trade.external.application.ports.operador_logistico_repository_port import OperadorLogisticoRepositoryPort
from ....trade.external.domain.models import Despachante

class DespachanteRepositoryPort(OperadorLogisticoRepositoryPort[Despachante]):
    pass