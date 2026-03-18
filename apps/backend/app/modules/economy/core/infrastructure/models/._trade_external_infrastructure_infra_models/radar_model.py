from __future__ import annotations
from apps.backend.app.core.db import Base
from ....trade.external.infrastructure.models.operador_logistico_columns_mixin import OperadorLogisticoColumnsMixin

class RadarModel(OperadorLogisticoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_radar'