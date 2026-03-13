from __future__ import annotations
from app.modules.resources.ambiente.domain.enums import TipoLicenca
from app.modules.resources.ambiente.domain.models.licenca_ambiental import LicencaAmbiental

class LicencaOperacao(LicencaAmbiental):

    @classmethod
    def requerer(cls, *, numero_car: str, atividade: str) -> 'LicencaOperacao':
        return cls.criar(numero_car=numero_car, tipo=TipoLicenca.OPERACAO, atividade=atividade)