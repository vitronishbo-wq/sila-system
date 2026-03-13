from __future__ import annotations
from app.modules.resources.ambiente.domain.enums import TipoEstudoAmbiental
from app.modules.resources.ambiente.domain.models.estudo_impacto import EstudoImpacto

class RIMA(EstudoImpacto):

    @classmethod
    def submeter(cls, *, numero_licenca: str, descricao: str, responsavel_tecnico: str) -> 'RIMA':
        return cls(**EstudoImpacto.submeter(numero_licenca=numero_licenca, tipo=TipoEstudoAmbiental.RIMA, descricao=descricao, responsavel_tecnico=responsavel_tecnico).__dict__)