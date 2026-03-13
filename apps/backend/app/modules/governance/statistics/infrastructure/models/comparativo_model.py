from app.core.db import Base
from app.modules.governance.statistics.infrastructure.models._generic_named_model import GenericNamedColumns

class ComparativoModel(GenericNamedColumns, Base):
    __tablename__ = 'est_comparativos'