"""Compatibility exports for emprego repositories."""
from app.modules.society.emprego.infrastructure.repositories import SQLAlchemyCandidatoRepository
Repository = SQLAlchemyCandidatoRepository
__all__ = ['SQLAlchemyCandidatoRepository', 'Repository']