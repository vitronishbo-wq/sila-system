from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.saude_juvenil_repository_port import SaudeJuvenilRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import StatusAcompanhamento, TipoSaudeJuvenil
from apps.backend.app.modules.society.juventude.domain.models.saude_juvenil import SaudeJuvenil

class SaudeJuvenilService:

    def __init__(self, *, saude_repo: SaudeJuvenilRepositoryPort, jovem_repo: JovemRepositoryPort) -> None:
        self.saude_repo = saude_repo
        self.jovem_repo = jovem_repo

    async def registrar_saude(self, *, jovem_id: UUID, tipo_registo: TipoSaudeJuvenil, descricao: str, data_registo: date, encaminhamento_necessario: bool=False, observacoes: str | None=None) -> SaudeJuvenil:
        if await self.jovem_repo.get_by_id(jovem_id) is None:
            raise ValueError('Jovem nao encontrado para registo de saude')
        codigo = await self.saude_repo.next_codigo()
        item = SaudeJuvenil.registrar(codigo_registo=codigo, jovem_id=jovem_id, tipo_registo=tipo_registo, descricao=descricao, data_registo=data_registo, encaminhamento_necessario=encaminhamento_necessario, observacoes=observacoes)
        return await self.saude_repo.save(item)

    async def buscar_registo(self, registo_id: UUID) -> SaudeJuvenil:
        item = await self.saude_repo.get_by_id(registo_id)
        if item is None:
            raise ValueError('Registo de saude nao encontrado')
        return item

    async def listar_registos(self, *, jovem_id: UUID | None=None, status: StatusAcompanhamento | None=None) -> list[SaudeJuvenil]:
        if jovem_id is not None:
            return await self.saude_repo.list_by_jovem(jovem_id)
        if status is not None:
            return await self.saude_repo.list_by_status(status)
        return await self.saude_repo.list_all()

    async def atualizar_acompanhamento(self, *, registo_id: UUID, status: StatusAcompanhamento) -> SaudeJuvenil:
        item = await self.buscar_registo(registo_id)
        item.atualizar_acompanhamento(status)
        return await self.saude_repo.save(item)

    async def remover_registo(self, registo_id: UUID) -> None:
        if not await self.saude_repo.delete(registo_id):
            raise ValueError('Registo de saude nao encontrado')