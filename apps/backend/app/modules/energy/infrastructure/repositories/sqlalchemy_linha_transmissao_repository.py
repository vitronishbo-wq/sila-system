from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import LinhaTransmissaoRepositoryPort
from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia
from apps.backend.app.modules.energy.domain.models import LinhaTransmissao
from apps.backend.app.modules.energy.infrastructure.models import LinhaTransmissaoModel

class SQLAlchemyLinhaTransmissaoRepository(LinhaTransmissaoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, LinhaTransmissaoModel] = {}

    async def save(self, item: LinhaTransmissao) -> LinhaTransmissao:
        model = LinhaTransmissaoModel(id=item.id, origem_id=item.origem_id, origem_tipo=item.origem_tipo, destino_id=item.destino_id, destino_tipo=item.destino_tipo, capacidade_mw=item.capacidade_mw, extensao_km=item.extensao_km, status=item.status, data_inicio_construcao=item.data_inicio_construcao, data_inicio_operacao=item.data_inicio_operacao)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> LinhaTransmissao | None:
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusInfraEnergia | None=None) -> list[LinhaTransmissao]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        return [self._to_domain(item) for item in values]

    async def list_all(self) -> list[LinhaTransmissao]:
        return await self.list()

    @staticmethod
    def _to_domain(model: LinhaTransmissaoModel) -> LinhaTransmissao:
        return LinhaTransmissao(id=model.id, origem_id=model.origem_id, origem_tipo=model.origem_tipo, destino_id=model.destino_id, destino_tipo=model.destino_tipo, capacidade_mw=model.capacidade_mw, extensao_km=model.extensao_km, status=model.status, data_inicio_construcao=model.data_inicio_construcao, data_inicio_operacao=model.data_inicio_operacao, observacoes=None)