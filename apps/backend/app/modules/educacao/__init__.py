"""Educacao module - matriculas escolares e catalogo institucional."""

from app.modules.educacao.api.router import router
from app.modules.educacao.application.services import InscricaoService, MatriculaService
from app.modules.educacao.infrastructure.models import (
    AnoLetivoModel,
    EscolaModel,
    InscricaoModel,
    MatriculaModel,
    TurmaModel,
)

__all__ = [
    "router",
    "MatriculaService",
    "InscricaoService",
    "MatriculaModel",
    "InscricaoModel",
    "EscolaModel",
    "TurmaModel",
    "AnoLetivoModel",
]
