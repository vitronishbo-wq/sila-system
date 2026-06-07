from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports.operador_logistico_repository_port import (
    OperadorLogisticoRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.models import TransportadorInternacional


class TransportadorInternacionalRepositoryPort(
    OperadorLogisticoRepositoryPort[TransportadorInternacional]
):
    pass
