from apps.backend.app.modules.governance.administracao_local.domain.entities import (
    AdministradorLocal,
)
from apps.backend.app.modules.governance.administracao_local.infrastructure.models import (
    AdministradorModel,
)


class AdministradorMapper:
    @staticmethod
    def to_domain(model: AdministradorModel) -> AdministradorLocal:
        return AdministradorLocal(id=model.id, nome=model.nome, cargo=model.cargo)

    @staticmethod
    def to_model(entity: AdministradorLocal) -> AdministradorModel:
        return AdministradorModel(id=entity.id, nome=entity.nome, cargo=entity.cargo)
