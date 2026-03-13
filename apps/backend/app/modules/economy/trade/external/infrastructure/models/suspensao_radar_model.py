from __future__ import annotations
from app.core.db import Base
from app.modules.economy.trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin

class SuspensaoRadarModel(HabilitacaoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_suspensoes_radar'