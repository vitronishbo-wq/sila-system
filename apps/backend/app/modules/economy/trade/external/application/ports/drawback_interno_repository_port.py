from __future__ import annotations

from apps.backend.app.modules.economy.trade.external.application.ports.habilitacao_repository_port_base import (
    HabilitacaoRepositoryPortBase,
)
from apps.backend.app.modules.economy.trade.external.domain.models import DrawbackInterno


class DrawbackInternoRepositoryPort(HabilitacaoRepositoryPortBase[DrawbackInterno]):
    pass
