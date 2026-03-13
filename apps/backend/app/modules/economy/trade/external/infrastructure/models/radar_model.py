from __future__ import annotations
from app.core.db import Base
from app.modules.economy.trade.external.infrastructure.models.operador_logistico_columns_mixin import OperadorLogisticoColumnsMixin

class RadarModel(OperadorLogisticoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_radar'