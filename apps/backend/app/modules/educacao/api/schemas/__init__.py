from .boletim_schema import BoletimCancelar, BoletimConcluir, BoletimCreate, BoletimResponse
from .certificado_schema import CertificadoCancelar, CertificadoConcluir, CertificadoCreate, CertificadoResponse
from .concurso_schema import ConcursoCancelar, ConcursoConcluir, ConcursoCreate, ConcursoResponse
from .emprego_schema import EmpregoCancelar, EmpregoConcluir, EmpregoCreate, EmpregoResponse
from .escola_schema import EscolaResponse
from .formacao_schema import FormacaoCancelar, FormacaoConcluir, FormacaoCreate, FormacaoResponse
from .inscricao_schema import InscricaoCancelar, InscricaoConfirmar, InscricaoCreate, InscricaoResponse
from .matricula_schema import MatriculaAtivar, MatriculaCreate, MatriculaListFilter, MatriculaResponse
from .propina_schema import PropinaCancelar, PropinaConcluir, PropinaCreate, PropinaResponse
from .transferencia_schema import TransferenciaCancelar, TransferenciaConcluir, TransferenciaCreate, TransferenciaResponse
from .universidade_schema import UniversidadeCancelar, UniversidadeConcluir, UniversidadeCreate, UniversidadeResponse
from .workflow_schema import WorkflowCancelar, WorkflowConcluir, WorkflowCreate, WorkflowResponse

__all__ = [
    "MatriculaCreate",
    "MatriculaAtivar",
    "MatriculaResponse",
    "MatriculaListFilter",
    "EscolaResponse",
    "InscricaoCreate",
    "InscricaoConfirmar",
    "InscricaoCancelar",
    "InscricaoResponse",
    "WorkflowCreate",
    "WorkflowConcluir",
    "WorkflowCancelar",
    "WorkflowResponse",
    "BoletimCreate",
    "BoletimConcluir",
    "BoletimCancelar",
    "BoletimResponse",
    "CertificadoCreate",
    "CertificadoConcluir",
    "CertificadoCancelar",
    "CertificadoResponse",
    "TransferenciaCreate",
    "TransferenciaConcluir",
    "TransferenciaCancelar",
    "TransferenciaResponse",
    "PropinaCreate",
    "PropinaConcluir",
    "PropinaCancelar",
    "PropinaResponse",
    "EmpregoCreate",
    "EmpregoConcluir",
    "EmpregoCancelar",
    "EmpregoResponse",
    "ConcursoCreate",
    "ConcursoConcluir",
    "ConcursoCancelar",
    "ConcursoResponse",
    "FormacaoCreate",
    "FormacaoConcluir",
    "FormacaoCancelar",
    "FormacaoResponse",
    "UniversidadeCreate",
    "UniversidadeConcluir",
    "UniversidadeCancelar",
    "UniversidadeResponse",
]
