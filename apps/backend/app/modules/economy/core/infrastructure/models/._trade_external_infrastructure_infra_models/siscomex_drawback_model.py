from __future__ import annotations
from apps.backend.app.core.db import Base
from ....trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin

class SiscomexDrawbackModel(HabilitacaoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_siscomex_drawback'