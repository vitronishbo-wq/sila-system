"""Compatibility layer for educacao services."""
from apps.backend.app.modules.educacao.application.matricula_service import MatriculaService
EducacaoService = MatriculaService
__all__ = ['MatriculaService', 'EducacaoService']
