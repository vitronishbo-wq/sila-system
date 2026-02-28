from app.modules.educacao.infrastructure.models import (
    AnoLetivoModel,
    EscolaModel,
    MatriculaModel,
    TurmaModel,
)
from app.modules.educacao.infrastructure.repositories import (
    SQLAlchemyEscolaRepository,
    SQLAlchemyMatriculaRepository,
)

__all__ = [
    "MatriculaModel",
    "EscolaModel",
    "TurmaModel",
    "AnoLetivoModel",
    "SQLAlchemyMatriculaRepository",
    "SQLAlchemyEscolaRepository",
]
