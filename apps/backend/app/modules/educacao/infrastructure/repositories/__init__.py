from .sqlalchemy_boletim_repository import SQLAlchemyBoletimRepository
from .sqlalchemy_certificado_repository import SQLAlchemyCertificadoRepository
from .sqlalchemy_concurso_repository import SQLAlchemyConcursoRepository
from .sqlalchemy_emprego_repository import SQLAlchemyEmpregoRepository
from .sqlalchemy_escola_repository import SQLAlchemyEscolaRepository
from .sqlalchemy_formacao_repository import SQLAlchemyFormacaoRepository
from .sqlalchemy_inscricao_repository import SQLAlchemyInscricaoRepository
from .sqlalchemy_matricula_repository import SQLAlchemyMatriculaRepository
from .sqlalchemy_propina_repository import SQLAlchemyPropinaRepository
from .sqlalchemy_transferencia_repository import SQLAlchemyTransferenciaRepository
from .sqlalchemy_universidade_repository import SQLAlchemyUniversidadeRepository

__all__ = [
    "SQLAlchemyMatriculaRepository",
    "SQLAlchemyEscolaRepository",
    "SQLAlchemyInscricaoRepository",
    "SQLAlchemyBoletimRepository",
    "SQLAlchemyCertificadoRepository",
    "SQLAlchemyTransferenciaRepository",
    "SQLAlchemyPropinaRepository",
    "SQLAlchemyEmpregoRepository",
    "SQLAlchemyConcursoRepository",
    "SQLAlchemyFormacaoRepository",
    "SQLAlchemyUniversidadeRepository",
]
