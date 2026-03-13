from __future__ import annotations
from app.core.db import Base
from app.modules.economy.trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin

class DrawbackVerdeAmareloModel(HabilitacaoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_drawback_verde_amarelo'