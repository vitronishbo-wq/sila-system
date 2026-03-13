"""Shared model aliases for society statistical data sources."""
from app.modules.society.assistencia_social.infrastructure.models.beneficiario_model import BeneficiarioModel
from app.modules.society.assistencia_social.infrastructure.models.beneficio_model import BeneficioModel
from app.modules.society.assistencia_social.infrastructure.models.cadastro_unico_model import CadastroUnicoModel
from app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel
from app.modules.educacao.infrastructure.models.propina_model import PropinaModel
from app.modules.educacao.infrastructure.models.turma_model import TurmaModel
from app.modules.society.emprego.infrastructure.models.candidato_model import CandidatoModel
from app.modules.society.emprego.infrastructure.models.contrato_model import ContratoModel
from app.modules.society.emprego.infrastructure.models.oferta_model import OfertaModel
from app.modules.society.juventude.infrastructure.models.auxilio_model import AuxilioModel
from app.modules.society.juventude.infrastructure.models.bolsa_estudo_model import BolsaEstudoModel
from app.modules.society.juventude.infrastructure.models.jovem_model import JovemModel
from app.modules.society.juventude.infrastructure.models.programa_juvenil_model import ProgramaJuvenilModel
from app.modules.saude.infrastructure.models import (
    AppointmentModel,
    HealthUnitModel,
    InternamentoModel,
    VaccineDoseModel,
)
__all__ = ['AppointmentModel', 'AuxilioModel', 'BeneficiarioModel', 'BeneficioModel', 'BolsaEstudoModel', 'CadastroUnicoModel', 'CandidatoModel', 'ContratoModel', 'HealthUnitModel', 'InternamentoModel', 'JovemModel', 'MatriculaModel', 'OfertaModel', 'PropinaModel', 'ProgramaJuvenilModel', 'TurmaModel', 'VaccineDoseModel']
