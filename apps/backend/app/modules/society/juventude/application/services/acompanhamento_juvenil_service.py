from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.society.juventude.application.ports.acompanhamento_juvenil_repository_port import AcompanhamentoJuvenilRepositoryPort
from app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from app.modules.society.juventude.domain.enums import StatusAcompanhamento
from app.modules.society.juventude.domain.models.acompanhamento_juvenil import AcompanhamentoJuvenil

class AcompanhamentoJuvenilService:

    def __init__(self, *, acompanhamento_repo: AcompanhamentoJuvenilRepositoryPort, jovem_repo: JovemRepositoryPort) -> None:
        self.acompanhamento_repo = acompanhamento_repo
        self.jovem_repo = jovem_repo

    async def abrir_acompanhamento(self, *, jovem_id: UUID, responsavel: str, objetivo: str, data_inicio: date, proxima_revisao: date | None=None, observacoes: str | None=None) -> AcompanhamentoJuvenil:
        if await self.jovem_repo.get_by_id(jovem_id) is None:
            raise ValueError('Jovem nao encontrado para acompanhamento')
        codigo = await self.acompanhamento_repo.next_codigo()
        item = AcompanhamentoJuvenil.abrir(codigo_acompanhamento=codigo, jovem_id=jovem_id, responsavel=responsavel, objetivo=objetivo, data_inicio=data_inicio, proxima_revisao=proxima_revisao, observacoes=observacoes)
        return await self.acompanhamento_repo.save(item)

    async def buscar_acompanhamento(self, acompanhamento_id: UUID) -> AcompanhamentoJuvenil:
        item = await self.acompanhamento_repo.get_by_id(acompanhamento_id)
        if item is None:
            raise ValueError('Acompanhamento nao encontrado')
        return item

    async def listar_acompanhamentos(self, *, jovem_id: UUID | None=None, status: StatusAcompanhamento | None=None) -> list[AcompanhamentoJuvenil]:
        if jovem_id is not None:
            return await self.acompanhamento_repo.list_by_jovem(jovem_id)
        if status is not None:
            return await self.acompanhamento_repo.list_by_status(status)
        return await self.acompanhamento_repo.list_all()

    async def registrar_evolucao(self, *, acompanhamento_id: UUID, descricao: str, proxima_revisao: date | None=None) -> AcompanhamentoJuvenil:
        item = await self.buscar_acompanhamento(acompanhamento_id)
        item.registrar_evolucao(descricao, proxima_revisao)
        return await self.acompanhamento_repo.save(item)

    async def encerrar_acompanhamento(self, *, acompanhamento_id: UUID, observacoes: str | None=None) -> AcompanhamentoJuvenil:
        item = await self.buscar_acompanhamento(acompanhamento_id)
        item.encerrar(observacoes)
        return await self.acompanhamento_repo.save(item)

    async def remover_acompanhamento(self, acompanhamento_id: UUID) -> None:
        if not await self.acompanhamento_repo.delete(acompanhamento_id):
            raise ValueError('Acompanhamento nao encontrado')