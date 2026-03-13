from __future__ import annotations
from app.domain.db import Base
from apps.backend.app.modules.economy.trade.external.infrastructure.models.operador_logistico_columns_mixin import OperadorLogisticoColumnsMixin

class TransportadorInternacionalModel(OperadorLogisticoColumnsMixin, Base):
    __tablename__ = 'comercio_externo_transportadores_internacionais'