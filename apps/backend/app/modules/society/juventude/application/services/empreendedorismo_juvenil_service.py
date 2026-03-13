from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.society.juventude.application.ports.empreendedorismo_juvenil_repository_port import EmpreendedorismoJuvenilRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusEmpreendimento
from apps.backend.app.modules.society.juventude.domain.models.empreendedorismo_juvenil import EmpreendedorismoJuvenil

class EmpreendedorismoJuvenilService:

    def __init__(self, *, empreendedorismo_repo: EmpreendedorismoJuvenilRepositoryPort, jovem_repo: JovemRepositoryPort) -> None:
        self.empreendedorismo_repo = empreendedorismo_repo
        self.jovem_repo = jovem_repo

    async def registrar_empreendimento(self, *, jovem_id: UUID, nome_negocio: str, area_interesse: AreaInteresse, receita_mensal: Decimal | None=None, valor_credito: Decimal | None=None, observacoes: str | None=None) -> EmpreendedorismoJuvenil:
        if await self.jovem_repo.get_by_id(jovem_id) is None:
            raise ValueError('Jovem nao encontrado para registro de empreendimento')
        codigo = await self.empreendedorismo_repo.next_codigo()
        item = EmpreendedorismoJuvenil.registrar(codigo_empreendimento=codigo, jovem_id=jovem_id, nome_negocio=nome_negocio, area_interesse=area_interesse, receita_mensal=receita_mensal, valor_credito=valor_credito, observacoes=observacoes)
        return await self.empreendedorismo_repo.save(item)

    async def buscar_empreendimento(self, empreendimento_id: UUID) -> EmpreendedorismoJuvenil:
        item = await self.empreendedorismo_repo.get_by_id(empreendimento_id)
        if item is None:
            raise ValueError('Empreendimento nao encontrado')
        return item

    async def listar_empreendimentos(self, *, jovem_id: UUID | None=None, status: StatusEmpreendimento | None=None) -> list[EmpreendedorismoJuvenil]:
        if jovem_id is not None:
            return await self.empreendedorismo_repo.list_by_jovem(jovem_id)
        if status is not None:
            return await self.empreendedorismo_repo.list_by_status(status)
        return await self.empreendedorismo_repo.list_all()

    async def atualizar_status(self, *, empreendimento_id: UUID, status: StatusEmpreendimento) -> EmpreendedorismoJuvenil:
        item = await self.buscar_empreendimento(empreendimento_id)
        item.atualizar_status(status)
        return await self.empreendedorismo_repo.save(item)

    async def remover_empreendimento(self, empreendimento_id: UUID) -> None:
        if not await self.empreendedorismo_repo.delete(empreendimento_id):
            raise ValueError('Empreendimento nao encontrado')