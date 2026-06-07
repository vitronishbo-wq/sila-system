from apps.backend.app.core.db import Base
from apps.backend.app.modules.governance.statistics.infrastructure.models._generic_named_model import (
    GenericNamedColumns,
)


class ExportacaoModel(GenericNamedColumns, Base):
    __tablename__ = "est_exportacoes"
