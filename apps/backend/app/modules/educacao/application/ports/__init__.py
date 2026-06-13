from __future__ import annotations

# Re-export repository port interfaces for the educacao application layer.
# Individual port implementations import from this package, so keep
# lightweight imports only (these modules contain ABCs only).
from .academic_identity_repository_port import AcademicIdentityRepositoryPort
from .boletim_repository_port import BoletimRepositoryPort
from .capacity_repository_port import CapacityRepositoryPort
from .certificado_repository_port import CertificadoRepositoryPort
from .concurso_repository_port import ConcursoRepositoryPort
from .emprego_repository_port import EmpregoRepositoryPort
from .enrollment_repository_port import EnrollmentRepositoryPort
from .escola_repository_port import EscolaRepositoryPort
from .formacao_repository_port import FormacaoRepositoryPort
from .guardian_repository_port import GuardianRepositoryPort
from .identity_service_port import IdentityServicePort
from .inscricao_repository_port import InscricaoRepositoryPort
from .matricula_repository_port import MatriculaRepositoryPort
from .propina_repository_port import PropinaRepositoryPort
from .transfer_repository_port import TransferRepositoryPort
from .transferencia_repository_port import TransferenciaRepositoryPort
from .turma_repository_port import TurmaRepositoryPort
from .universidade_repository_port import UniversidadeRepositoryPort
from .wizard_session_repository_port import WizardSessionRepositoryPort
from .workflow_repository_port import WorkflowRepositoryPort

__all__ = [
    "AcademicIdentityRepositoryPort",
    "BoletimRepositoryPort",
    "CapacityRepositoryPort",
    "CertificadoRepositoryPort",
    "ConcursoRepositoryPort",
    "EmpregoRepositoryPort",
    "EnrollmentRepositoryPort",
    "EscolaRepositoryPort",
    "FormacaoRepositoryPort",
    "GuardianRepositoryPort",
    "IdentityServicePort",
    "InscricaoRepositoryPort",
    "MatriculaRepositoryPort",
    "PropinaRepositoryPort",
    "TransferRepositoryPort",
    "TransferenciaRepositoryPort",
    "TurmaRepositoryPort",
    "UniversidadeRepositoryPort",
    "WizardSessionRepositoryPort",
    "WorkflowRepositoryPort",
]
