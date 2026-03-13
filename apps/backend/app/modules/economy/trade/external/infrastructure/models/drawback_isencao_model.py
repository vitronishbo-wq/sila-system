from __future__ import annotations
from app.core.db import Base
from apps.backend.app.modules.economy.trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin

class DrawbackIsencaoModel(HabilitacaoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_drawback_isencao'