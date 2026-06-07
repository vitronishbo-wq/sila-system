from apps.backend.app.modules.resources.ambiente.domain.models.auto_infracao import AutoInfracao
from apps.backend.app.modules.resources.ambiente.domain.models.car import CAR
from apps.backend.app.modules.resources.ambiente.domain.models.condicionante import Condicionante
from apps.backend.app.modules.resources.ambiente.domain.models.eia import EIA
from apps.backend.app.modules.resources.ambiente.domain.models.embargo import Embargo
from apps.backend.app.modules.resources.ambiente.domain.models.estudo_impacto import EstudoImpacto
from apps.backend.app.modules.resources.ambiente.domain.models.fiscalizacao import Fiscalizacao
from apps.backend.app.modules.resources.ambiente.domain.models.imovel_rural import ImovelRural
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_ambiental import (
    LicencaAmbiental,
)
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_instalacao import (
    LicencaInstalacao,
)
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_operacao import (
    LicencaOperacao,
)
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_previa import LicencaPrevia
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_unica import LicencaUnica
from apps.backend.app.modules.resources.ambiente.domain.models.multa import Multa
from apps.backend.app.modules.resources.ambiente.domain.models.proprietario import Proprietario
from apps.backend.app.modules.resources.ambiente.domain.models.rima import RIMA

__all__ = [
    "Proprietario",
    "ImovelRural",
    "CAR",
    "LicencaAmbiental",
    "LicencaPrevia",
    "LicencaInstalacao",
    "LicencaOperacao",
    "LicencaUnica",
    "EstudoImpacto",
    "EIA",
    "RIMA",
    "Condicionante",
    "Fiscalizacao",
    "AutoInfracao",
    "Embargo",
    "Multa",
]
