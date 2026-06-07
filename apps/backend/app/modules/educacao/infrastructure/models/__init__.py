from .academic_identity_model import AcademicIdentityModel
from .academic_record_model import AcademicRecordModel
from .ano_letivo_model import AnoLetivoModel
from .boletim_model import BoletimModel
from .certificado_model import CertificadoModel
from .concurso_model import ConcursoModel
from .emprego_model import EmpregoModel
from .enrollment_model import EnrollmentModel
from .escola_model import EscolaModel
from .formacao_model import FormacaoModel
from .inscricao_model import InscricaoModel
from .institution_capacity_model import InstitutionCapacityModel
from .matricula_model import MatriculaModel
from .propina_model import PropinaModel
from .transfer_model import TransferModel
from .transferencia_model import TransferenciaModel
from .turma_model import TurmaModel
from .universidade_model import UniversidadeModel
from .wizard_session_model import WizardSessionModel
from .guardian_model import GuardianModel
from .guardian_student_link import GuardianStudentLink
from .identity_merge_model import IdentityMergeModel
from .student_number_counter import StudentNumberCounter

__all__ = [
    "MatriculaModel",
    "EscolaModel",
    "TurmaModel",
    "AnoLetivoModel",
    "InscricaoModel",
    "BoletimModel",
    "CertificadoModel",
    "TransferenciaModel",
    "PropinaModel",
    "EmpregoModel",
    "ConcursoModel",
    "FormacaoModel",
    "UniversidadeModel",
    "AcademicIdentityModel",
    "AcademicRecordModel",
    "EnrollmentModel",
    "TransferModel",
    "InstitutionCapacityModel",
    "WizardSessionModel",
    "GuardianModel",
    "GuardianStudentLink",
    "IdentityMergeModel",
    "StudentNumberCounter",
]
