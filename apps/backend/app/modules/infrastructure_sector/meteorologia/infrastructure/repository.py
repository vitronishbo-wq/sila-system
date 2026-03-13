"""Compatibility exports for legacy imports."""
from app.modules.infrastructure_sector.meteorologia.infrastructure.repositories import SQLAlchemyEstacaoRepository, SQLAlchemyObservacaoRepository
__all__ = ['SQLAlchemyEstacaoRepository', 'SQLAlchemyObservacaoRepository']