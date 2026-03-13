from __future__ import annotations
from typing import Any
from apps.backend.app.modules.governance.statistics.application.ports.named_entity_repository_port import NamedEntityRepositoryPort
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

class NamedEntityService:

    def __init__(self, repository: NamedEntityRepositoryPort, entity_label: str) -> None:
        self.repository = repository
        self.entity_label = entity_label

    async def criar(self, data: dict[str, Any]) -> Any:
        return await self.repository.create(data)

    async def listar(self, limit: int=100, offset: int=0) -> list[Any]:
        return await self.repository.list_all(limit=limit, offset=offset)

    async def obter(self, entity_id: int) -> Any:
        entity = await self.repository.get_by_id(entity_id)
        if entity is None:
            raise EstatisticaNotFoundError(f'{self.entity_label} nao encontrado')
        return entity

    async def atualizar(self, entity_id: int, data: dict[str, Any]) -> Any:
        updated = await self.repository.update(entity_id, data)
        if updated is None:
            raise EstatisticaNotFoundError(f'{self.entity_label} nao encontrado')
        return updated

    async def deletar(self, entity_id: int) -> None:
        deleted = await self.repository.delete(entity_id)
        if not deleted:
            raise EstatisticaNotFoundError(f'{self.entity_label} nao encontrado')