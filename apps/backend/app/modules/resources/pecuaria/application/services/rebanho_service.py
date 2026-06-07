from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.resources.pecuaria.application.ports import RebanhoRepositoryPort
from apps.backend.app.modules.resources.pecuaria.domain.enums import TipoAnimal
from apps.backend.app.modules.resources.pecuaria.domain.models.rebanho import Rebanho


class RebanhoService:
    def __init__(self, repository: RebanhoRepositoryPort):
        self._repository = repository

    async def cadastrar(
        self,
        *,
        propriedade_id: UUID,
        tipo_animal: TipoAnimal,
        descricao: str,
        quantidade_animais: int = 0,
    ) -> Rebanho:
        item = Rebanho.criar(
            propriedade_id=propriedade_id,
            tipo_animal=tipo_animal,
            descricao=descricao,
            quantidade_animais=quantidade_animais,
        )
        item.codigo_rebanho = await self._repository.next_codigo()
        return await self._repository.save(item)

    async def obter(self, codigo_rebanho: str) -> Rebanho:
        item = await self._repository.get_by_codigo(codigo_rebanho)
        if not item:
            raise ValueError("Rebanho nao encontrado")
        return item

    async def listar(self, propriedade_id: UUID | None = None) -> list[Rebanho]:
        return await self._repository.list_by_propriedade(propriedade_id=propriedade_id)
