from __future__ import annotations
from apps.backend.app.core.db import Base
from ....trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin

class DrawbackVerdeAmareloModel(HabilitacaoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_drawback_verde_amarelo'