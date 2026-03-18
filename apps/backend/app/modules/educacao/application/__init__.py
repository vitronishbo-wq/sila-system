"""Educacao application layer - ports and interfaces"""
from apps.backend.app.modules.educacao.application.ports import EscolaRepositoryPort, MatriculaRepositoryPort, TurmaRepositoryPort
__all__ = ['MatriculaRepositoryPort', 'TurmaRepositoryPort', 'EscolaRepositoryPort']