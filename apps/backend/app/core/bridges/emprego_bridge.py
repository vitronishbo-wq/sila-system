"""Emprego bridge exports to avoid direct module-to-module imports."""

from apps.backend.app.modules.society.emprego.application.ports import CandidatoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.repositories import (
    SQLAlchemyCandidatoRepository,
)

__all__ = ["CandidatoRepositoryPort", "SQLAlchemyCandidatoRepository"]
