from __future__ import annotations
from app.domain.db import Base
from apps.backend.app.modules.economy.trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin

class HabilitacaoImportadorModel(HabilitacaoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_habilitacoes_importador'