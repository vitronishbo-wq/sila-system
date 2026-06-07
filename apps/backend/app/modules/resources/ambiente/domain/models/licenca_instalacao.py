from __future__ import annotations

from apps.backend.app.modules.resources.ambiente.domain.enums import TipoLicenca
from apps.backend.app.modules.resources.ambiente.domain.models.licenca_ambiental import (
    LicencaAmbiental,
)


class LicencaInstalacao(LicencaAmbiental):
    @classmethod
    def requerer(cls, *, numero_car: str, atividade: str) -> LicencaInstalacao:
        return cls.criar(numero_car=numero_car, tipo=TipoLicenca.INSTALACAO, atividade=atividade)
