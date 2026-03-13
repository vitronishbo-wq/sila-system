"""Shared enum aliases for society domain integration points."""
from app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade, StatusBeneficio as StatusBeneficioAssistencia, SituacaoBeneficiario, TipoBeneficio
from app.core.enums import StatusMatricula
from app.modules.educacao.domain.models.turma import Turno
from app.modules.society.emprego.domain.enums import Escolaridade as EscolaridadeEmprego
from app.modules.society.emprego.domain.enums import SituacaoProfissional, StatusCandidato
from app.modules.society.juventude.domain.enums import Escolaridade as EscolaridadeJuventude, FaixaEtaria, StatusBeneficio as StatusBeneficioJuventude, SituacaoOcupacional, StatusPrograma, TipoAuxilio, TipoBolsa, TipoPrograma
from app.modules.saude.domain.enums import HealthUnitType
__all__ = ['EscolaridadeEmprego', 'EscolaridadeJuventude', 'FaixaEtaria', 'FaixaVulnerabilidade', 'HealthUnitType', 'SituacaoBeneficiario', 'SituacaoOcupacional', 'SituacaoProfissional', 'StatusBeneficioAssistencia', 'StatusBeneficioJuventude', 'StatusCandidato', 'StatusMatricula', 'StatusPrograma', 'TipoAuxilio', 'TipoBeneficio', 'TipoBolsa', 'TipoPrograma', 'Turno']
