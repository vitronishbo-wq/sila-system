"""Educacao module - matriculas escolares e catalogo institucional."""
from apps.backend.app.modules.educacao.infrastructure.models import AnoLetivoModel, BoletimModel, CertificadoModel, ConcursoModel, EmpregoModel, EscolaModel, FormacaoModel, InscricaoModel, MatriculaModel, PropinaModel, TransferenciaModel, TurmaModel, UniversidadeModel
__all__ = ['MatriculaModel', 'InscricaoModel', 'BoletimModel', 'CertificadoModel', 'TransferenciaModel', 'PropinaModel', 'EmpregoModel', 'ConcursoModel', 'FormacaoModel', 'UniversidadeModel', 'EscolaModel', 'TurmaModel', 'AnoLetivoModel']
HealthStatus = dict

async def startup() -> None:
    return None

async def shutdown() -> None:
    return None

def health_check() -> HealthStatus:
    return {'status': 'ok'}