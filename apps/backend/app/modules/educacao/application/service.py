"""Compatibility layer for educacao services."""

from app.modules.educacao.application.services import MatriculaService

EducacaoService = MatriculaService

__all__ = ["MatriculaService", "EducacaoService"]
