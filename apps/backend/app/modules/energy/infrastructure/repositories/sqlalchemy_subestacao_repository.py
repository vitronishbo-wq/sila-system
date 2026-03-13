from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import SubestacaoRepositoryPort
from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia
from apps.backend.app.modules.energy.domain.models import Subestacao
from apps.backend.app.modules.energy.infrastructure.models import SubestacaoModel

class SQLAlchemySubestacaoRepository(SubestacaoRepositoryPort):
    """In-memory implementation with SQLAlchemy naming for progressive migration."""

    def __init__(self) -> None:
        self._items: dict[UUID, SubestacaoModel] = {}

    async def save(self, item: Subestacao) -> Subestacao:
        model = SubestacaoModel(id=item.id, nome=item.nome, tensao_nominal_kv=item.tensao_nominal_kv, classe_tensao=item.classe_tensao, municipio=item.municipio, provincia=item.provincia, status=item.status, data_inicio_construcao=item.data_inicio_construcao, data_inicio_operacao=item.data_inicio_operacao)
        self._items[model.id] = model
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> Subestacao | None:
        model = self._items.get(id)
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusInfraEnergia | None=None) -> list[Subestacao]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        values.sort(key=lambda item: item.nome.lower())
        return [self._to_domain(item) for item in values]

    async def list_all(self) -> list[Subestacao]:
        return await self.list()

    @staticmethod
    def _to_domain(model: SubestacaoModel) -> Subestacao:
        return Subestacao(id=model.id, nome=model.nome, tensao_nominal_kv=model.tensao_nominal_kv, classe_tensao=model.classe_tensao, municipio=model.municipio, provincia=model.provincia, status=model.status, data_inicio_construcao=model.data_inicio_construcao, data_inicio_operacao=model.data_inicio_operacao, observacoes=None)
