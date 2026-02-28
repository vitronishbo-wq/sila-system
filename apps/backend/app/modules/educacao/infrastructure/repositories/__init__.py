from .sqlalchemy_escola_repository import SQLAlchemyEscolaRepository
from .sqlalchemy_inscricao_repository import SQLAlchemyInscricaoRepository
from .sqlalchemy_matricula_repository import SQLAlchemyMatriculaRepository

__all__ = [
    "SQLAlchemyMatriculaRepository",
    "SQLAlchemyEscolaRepository",
    "SQLAlchemyInscricaoRepository",
]
