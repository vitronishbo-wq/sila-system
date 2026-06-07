"""Shared enum aliases for society domain integration points."""

from apps.backend.app.core.enums import StatusMatricula

from apps.backend.app.modules.educacao.domain.models.turma import Turno
from apps.backend.app.modules.saude.domain.enums import HealthUnitType
from apps.backend.app.modules.society.assistencia_social.domain.enums import (
    FaixaVulnerabilidade,
    SituacaoBeneficiario,
    StatusBeneficio as StatusBeneficioAssistencia,
    TipoBeneficio,
)
from apps.backend.app.modules.society.emprego.domain.enums import (
    Escolaridade as EscolaridadeEmprego,
    SituacaoProfissional,
    StatusCandidato,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    Escolaridade as EscolaridadeJuventude,
    FaixaEtaria,
    SituacaoOcupacional,
    StatusBeneficio as StatusBeneficioJuventude,
    StatusPrograma,
    TipoAuxilio,
    TipoBolsa,
    TipoPrograma,
)

__all__ = [
    "EscolaridadeEmprego",
    "EscolaridadeJuventude",
    "FaixaEtaria",
    "FaixaVulnerabilidade",
    "HealthUnitType",
    "SituacaoBeneficiario",
    "SituacaoOcupacional",
    "SituacaoProfissional",
    "StatusBeneficioAssistencia",
    "StatusBeneficioJuventude",
    "StatusCandidato",
    "StatusMatricula",
    "StatusPrograma",
    "TipoAuxilio",
    "TipoBeneficio",
    "TipoBolsa",
    "TipoPrograma",
    "Turno",
]
