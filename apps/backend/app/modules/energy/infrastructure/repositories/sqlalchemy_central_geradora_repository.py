from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import CentralGeradoraRepositoryPort
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusInfraEnergia
from apps.backend.app.modules.energy.domain.models import CentralGeradora
from apps.backend.app.modules.energy.infrastructure.models import CentralGeradoraModel

class SQLAlchemyCentralGeradoraRepository(CentralGeradoraRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, CentralGeradoraModel] = {}

    async def save(self, item: CentralGeradora) -> CentralGeradora:
        model = CentralGeradoraModel(id=item.id, nome=item.nome, tipo=item.tipo, capacidade_instalada_mw=item.capacidade_instalada_mw, municipio=item.municipio, provincia=item.provincia, status=item.status, data_inicio_construcao=item.data_inicio_construcao, data_inicio_operacao=item.data_inicio_operacao)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> CentralGeradora | None:
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusInfraEnergia | None=None, tipo: FonteEnergia | None=None) -> list[CentralGeradora]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def list_all(self) -> list[CentralGeradora]:
        return await self.list()

    @staticmethod
    def _to_domain(model: CentralGeradoraModel) -> CentralGeradora:
        return CentralGeradora(id=model.id, nome=model.nome, tipo=model.tipo, capacidade_instalada_mw=model.capacidade_instalada_mw, municipio=model.municipio, provincia=model.provincia, status=model.status, data_inicio_construcao=model.data_inicio_construcao, data_inicio_operacao=model.data_inicio_operacao, observacoes=None)
