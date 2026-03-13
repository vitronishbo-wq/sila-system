"""Educacao application layer - ports and interfaces"""
# Avoid circular imports: don't import concrete services in __init__
from app.modules.educacao.application.ports import EscolaRepositoryPort, MatriculaRepositoryPort, TurmaRepositoryPort
__all__ = ['MatriculaRepositoryPort', 'TurmaRepositoryPort', 'EscolaRepositoryPort']