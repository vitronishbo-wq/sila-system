from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.society.juventude.application.ports.intercambio_juvenil_repository_port import IntercambioJuvenilRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusIntercambio
from apps.backend.app.modules.society.juventude.domain.models.intercambio_juvenil import IntercambioJuvenil

class IntercambioJuvenilService:

    def __init__(self, *, intercambio_repo: IntercambioJuvenilRepositoryPort, jovem_repo: JovemRepositoryPort) -> None:
        self.intercambio_repo = intercambio_repo
        self.jovem_repo = jovem_repo

    async def solicitar_intercambio(self, *, jovem_id: UUID, pais_destino: str, instituicao_destino: str, area_interesse: AreaInteresse, data_inicio: date, data_fim: date | None=None, observacoes: str | None=None) -> IntercambioJuvenil:
        if await self.jovem_repo.get_by_id(jovem_id) is None:
            raise ValueError('Jovem nao encontrado para intercambio')
        codigo = await self.intercambio_repo.next_codigo()
        item = IntercambioJuvenil.solicitar(codigo_intercambio=codigo, jovem_id=jovem_id, pais_destino=pais_destino, instituicao_destino=instituicao_destino, area_interesse=area_interesse, data_inicio=data_inicio, data_fim=data_fim, observacoes=observacoes)
        return await self.intercambio_repo.save(item)

    async def buscar_intercambio(self, intercambio_id: UUID) -> IntercambioJuvenil:
        item = await self.intercambio_repo.get_by_id(intercambio_id)
        if item is None:
            raise ValueError('Intercambio nao encontrado')
        return item

    async def listar_intercambios(self, *, jovem_id: UUID | None=None, status: StatusIntercambio | None=None) -> list[IntercambioJuvenil]:
        if jovem_id is not None:
            return await self.intercambio_repo.list_by_jovem(jovem_id)
        if status is not None:
            return await self.intercambio_repo.list_by_status(status)
        return await self.intercambio_repo.list_all()

    async def atualizar_status(self, *, intercambio_id: UUID, status: StatusIntercambio) -> IntercambioJuvenil:
        item = await self.buscar_intercambio(intercambio_id)
        item.atualizar_status(status)
        return await self.intercambio_repo.save(item)

    async def remover_intercambio(self, intercambio_id: UUID) -> None:
        if not await self.intercambio_repo.delete(intercambio_id):
            raise ValueError('Intercambio nao encontrado')