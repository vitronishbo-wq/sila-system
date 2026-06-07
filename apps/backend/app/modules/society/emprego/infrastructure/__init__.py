from apps.backend.app.modules.society.emprego.infrastructure.models.candidato_model import (
    CandidatoModel,
)
from apps.backend.app.modules.society.emprego.infrastructure.repositories import (
    SQLAlchemyCandidatoRepository,
)

__all__ = ["CandidatoModel", "SQLAlchemyCandidatoRepository"]
