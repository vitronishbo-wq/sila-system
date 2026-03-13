from app.domain.db import Base
from apps.backend.app.modules.governance.statistics.infrastructure.models._generic_named_model import GenericNamedColumns

class TendenciaModel(GenericNamedColumns, Base):
    __tablename__ = 'est_tendencias'