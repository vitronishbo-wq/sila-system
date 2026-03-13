from __future__ import annotations
from uuid import UUID
from app.modules.resources.pecuaria.application.ports import PropriedadePecuariaRepositoryPort
from app.modules.resources.pecuaria.domain.models.propriedade_pecuaria import PropriedadePecuaria

class PropriedadeService:

    def __init__(self, repository: PropriedadePecuariaRepositoryPort):
        self._repository = repository

    async def cadastrar(self, *, pecuarista_id: UUID, nome: str, area_total_ha: float, municipio: str, provincia: str) -> PropriedadePecuaria:
        item = PropriedadePecuaria.criar(pecuarista_id=pecuarista_id, nome=nome, area_total_ha=area_total_ha, municipio=municipio, provincia=provincia)
        item.codigo_propriedade = await self._repository.next_codigo()
        return await self._repository.save(item)

    async def obter(self, codigo_propriedade: str) -> PropriedadePecuaria:
        item = await self._repository.get_by_codigo(codigo_propriedade)
        if not item:
            raise ValueError('Propriedade pecuaria nao encontrada')
        return item

    async def listar(self, pecuarista_id: UUID | None=None) -> list[PropriedadePecuaria]:
        return await self._repository.list_by_pecuarista(pecuarista_id=pecuarista_id)