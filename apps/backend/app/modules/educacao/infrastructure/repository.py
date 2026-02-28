"""Compatibility exports for educacao repositories."""

from app.modules.educacao.infrastructure.repositories import (
    SQLAlchemyEscolaRepository,
    SQLAlchemyMatriculaRepository,
)

Repository = SQLAlchemyMatriculaRepository

__all__ = ["SQLAlchemyMatriculaRepository", "SQLAlchemyEscolaRepository", "Repository"]
