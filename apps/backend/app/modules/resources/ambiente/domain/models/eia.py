from __future__ import annotations
from app.modules.resources.ambiente.domain.enums import TipoEstudoAmbiental
from app.modules.resources.ambiente.domain.models.estudo_impacto import EstudoImpacto

class EIA(EstudoImpacto):

    @classmethod
    def submeter(cls, *, numero_licenca: str, descricao: str, responsavel_tecnico: str) -> 'EIA':
        return cls.submeter_generico(numero_licenca=numero_licenca, tipo=TipoEstudoAmbiental.EIA, descricao=descricao, responsavel_tecnico=responsavel_tecnico)

    @classmethod
    def submeter_generico(cls, *, numero_licenca: str, tipo: TipoEstudoAmbiental, descricao: str, responsavel_tecnico: str) -> 'EIA':
        return cls(**EstudoImpacto.submeter(numero_licenca=numero_licenca, tipo=tipo, descricao=descricao, responsavel_tecnico=responsavel_tecnico).__dict__)