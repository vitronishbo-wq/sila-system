"""Cross-domain port aliases for economy integrations.

Importing ports through app.core keeps feature modules decoupled from each
other while preserving static contracts.
"""
from app.modules.governance.service_requests.application.ports.request_repository_port import RequestRepositoryPort
from app.modules.public_security.application.ports.ocorrencia_repository_port import OcorrenciaRepositoryPort
from app.modules.resources.agricultura.application.ports.produtor_repository_port import ProdutorRepositoryPort
from app.modules.society.assistencia_social.application.ports.beneficiario_repository_port import BeneficiarioRepositoryPort
from app.modules.society.assistencia_social.application.ports.beneficio_repository_port import BeneficioRepositoryPort
from app.modules.educacao.application.ports.matricula_repository_port import MatriculaRepositoryPort
from app.modules.educacao.application.ports.propina_repository_port import PropinaRepositoryPort
from app.modules.society.emprego.application.ports.candidato_repository_port import CandidatoRepositoryPort
from app.modules.society.emprego.application.ports.contrato_repository_port import ContratoRepositoryPort
from app.modules.society.juventude.application.ports.auxilio_repository_port import AuxilioRepositoryPort
from app.modules.society.juventude.application.ports.bolsa_estudo_repository_port import BolsaEstudoRepositoryPort
from app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from app.modules.saude.application.ports.appointment_repository_port import (
    AppointmentRepositoryPort,
)
from app.modules.saude.application.ports.health_unit_repository_port import (
    HealthUnitRepositoryPort,
)
__all__ = ['AppointmentRepositoryPort', 'AuxilioRepositoryPort', 'BeneficiarioRepositoryPort', 'BeneficioRepositoryPort', 'BolsaEstudoRepositoryPort', 'CandidatoRepositoryPort', 'ContratoRepositoryPort', 'HealthUnitRepositoryPort', 'JovemRepositoryPort', 'MatriculaRepositoryPort', 'OcorrenciaRepositoryPort', 'ProdutorRepositoryPort', 'PropinaRepositoryPort', 'RequestRepositoryPort']
