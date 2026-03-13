"""Emprego bridge exports to avoid direct module-to-module imports."""
from app.modules.society.emprego.application.ports import CandidatoRepositoryPort
from app.modules.society.emprego.infrastructure.repositories import SQLAlchemyCandidatoRepository
__all__ = ['CandidatoRepositoryPort', 'SQLAlchemyCandidatoRepository']