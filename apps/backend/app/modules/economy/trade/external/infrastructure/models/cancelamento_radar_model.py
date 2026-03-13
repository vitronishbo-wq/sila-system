from __future__ import annotations
from apps.backend.app.core.db import Base
from apps.backend.app.modules.economy.trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin

class CancelamentoRadarModel(HabilitacaoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_cancelamentos_radar'