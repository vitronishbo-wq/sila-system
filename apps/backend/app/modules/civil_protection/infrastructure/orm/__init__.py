from apps.backend.app.modules.civil_protection.infrastructure.orm.atendimento_model import (
    AtendimentoModel,
)
from apps.backend.app.modules.civil_protection.infrastructure.orm.bombeiro_model import (
    BombeiroModel,
)
from apps.backend.app.modules.civil_protection.infrastructure.orm.corporacao_model import (
    CorporacaoModel,
)
from apps.backend.app.modules.civil_protection.infrastructure.orm.despacho_model import (
    DespachoModel,
)
from apps.backend.app.modules.civil_protection.infrastructure.orm.ocorrencia_emergencial_model import (
    OcorrenciaEmergencialModel,
)

__all__ = [
    "CorporacaoModel",
    "BombeiroModel",
    "OcorrenciaEmergencialModel",
    "DespachoModel",
    "AtendimentoModel",
]
