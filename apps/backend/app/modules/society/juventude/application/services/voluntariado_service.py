from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.voluntariado_repository_port import VoluntariadoRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusVoluntariado
from apps.backend.app.modules.society.juventude.domain.models.voluntariado import Voluntariado

class VoluntariadoService:

    def __init__(self, *, voluntariado_repo: VoluntariadoRepositoryPort, jovem_repo: JovemRepositoryPort) -> None:
        self.voluntariado_repo = voluntariado_repo
        self.jovem_repo = jovem_repo

    async def iniciar_voluntariado(self, *, jovem_id: UUID, organizacao: str, causa: AreaInteresse, carga_horaria_total: int, data_inicio: date, data_fim: date | None=None, observacoes: str | None=None) -> Voluntariado:
        if await self.jovem_repo.get_by_id(jovem_id) is None:
            raise ValueError('Jovem nao encontrado para voluntariado')
        codigo = await self.voluntariado_repo.next_codigo()
        item = Voluntariado.iniciar(codigo_voluntariado=codigo, jovem_id=jovem_id, organizacao=organizacao, causa=causa, carga_horaria_total=carga_horaria_total, data_inicio=data_inicio, data_fim=data_fim, observacoes=observacoes)
        return await self.voluntariado_repo.save(item)

    async def buscar_voluntariado(self, voluntariado_id: UUID) -> Voluntariado:
        item = await self.voluntariado_repo.get_by_id(voluntariado_id)
        if item is None:
            raise ValueError('Voluntariado nao encontrado')
        return item

    async def listar_voluntariados(self, *, jovem_id: UUID | None=None, status: StatusVoluntariado | None=None) -> list[Voluntariado]:
        if jovem_id is not None:
            return await self.voluntariado_repo.list_by_jovem(jovem_id)
        if status is not None:
            return await self.voluntariado_repo.list_by_status(status)
        return await self.voluntariado_repo.list_all()

    async def atualizar_status(self, *, voluntariado_id: UUID, status: StatusVoluntariado) -> Voluntariado:
        item = await self.buscar_voluntariado(voluntariado_id)
        item.atualizar_status(status)
        return await self.voluntariado_repo.save(item)

    async def remover_voluntariado(self, voluntariado_id: UUID) -> None:
        if not await self.voluntariado_repo.delete(voluntariado_id):
            raise ValueError('Voluntariado nao encontrado')