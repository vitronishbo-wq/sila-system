from __future__ import annotations

from apps.backend.app.modules.resources.pescas.application.ports import ArmadorRepositoryPort
from apps.backend.app.modules.resources.pescas.domain.models.armador import Armador


class ArmadorService:
    def __init__(self, repository: ArmadorRepositoryPort):
        self.repository = repository

    async def cadastrar_armador(self, *, nome: str, nif: str) -> Armador:
        if await self.repository.get_by_nif(nif):
            raise ValueError("Armador com este NIF ja existe")
        return await self.repository.save(Armador.cadastrar(nome=nome, nif=nif))

    async def obter_armador(self, armador_id) -> Armador:
        item = await self.repository.get_by_id(armador_id)
        if not item:
            raise ValueError("Armador nao encontrado")
        return item

    async def listar_armadores(self, *, ativo: bool | None = None) -> list[Armador]:
        return await self.repository.list_all(ativo)
