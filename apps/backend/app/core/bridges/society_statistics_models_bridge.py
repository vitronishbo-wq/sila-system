"""Shared model aliases for society statistical data sources."""
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.beneficiario_model import BeneficiarioModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.beneficio_model import BeneficioModel
from apps.backend.app.modules.society.assistencia_social.infrastructure.models.cadastro_unico_model import CadastroUnicoModel
from apps.backend.app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel
from apps.backend.app.modules.educacao.infrastructure.models.propina_model import PropinaModel
from apps.backend.app.modules.educacao.infrastructure.models.turma_model import TurmaModel
from apps.backend.app.modules.society.emprego.infrastructure.models.candidato_model import CandidatoModel
from apps.backend.app.modules.society.emprego.infrastructure.models.contrato_model import ContratoModel
from apps.backend.app.modules.society.emprego.infrastructure.models.oferta_model import OfertaModel
from apps.backend.app.modules.society.juventude.infrastructure.models.auxilio_model import AuxilioModel
from apps.backend.app.modules.society.juventude.infrastructure.models.bolsa_estudo_model import BolsaEstudoModel
from apps.backend.app.modules.society.juventude.infrastructure.models.jovem_model import JovemModel
from apps.backend.app.modules.society.juventude.infrastructure.models.programa_juvenil_model import ProgramaJuvenilModel
from apps.backend.app.modules.saude.infrastructure.models import AppointmentModel, HealthUnitModel, InternamentoModel, VaccineDoseModel
__all__ = ['AppointmentModel', 'AuxilioModel', 'BeneficiarioModel', 'BeneficioModel', 'BolsaEstudoModel', 'CadastroUnicoModel', 'CandidatoModel', 'ContratoModel', 'HealthUnitModel', 'InternamentoModel', 'JovemModel', 'MatriculaModel', 'OfertaModel', 'PropinaModel', 'ProgramaJuvenilModel', 'TurmaModel', 'VaccineDoseModel']