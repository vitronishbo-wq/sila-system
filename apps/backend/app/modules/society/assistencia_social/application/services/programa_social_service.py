from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.society.assistencia_social.application.ports import ProgramaSocialRepositoryPort
from app.modules.society.assistencia_social.application.services._codegen import next_codigo
from app.modules.society.assistencia_social.domain.enums import PublicoAlvo
from app.modules.society.assistencia_social.domain.models import ProgramaSocial

class ProgramaSocialService:

    def __init__(self, *, programa_repo: ProgramaSocialRepositoryPort) -> None:
        self.programa_repo = programa_repo

    async def criar_programa(self, *, nome: str, publico_alvo: PublicoAlvo, criterio_renda_max: Decimal, valor_base: Decimal, vagas: int | None, data_inicio: date, observacoes: str | None=None) -> ProgramaSocial:
        codigo = next_codigo('PRG', len(await self.programa_repo.list_all()))
        programa = ProgramaSocial.criar(codigo=codigo, nome=nome, publico_alvo=publico_alvo, criterio_renda_max=criterio_renda_max, valor_base=valor_base, vagas=vagas, data_inicio=data_inicio, observacoes=observacoes)
        return await self.programa_repo.save(programa)

    async def buscar_programa(self, programa_id: UUID) -> ProgramaSocial:
        item = await self.programa_repo.get_by_id(programa_id)
        if item is None:
            raise ValueError('Programa social nao encontrado')
        return item

    async def listar_programas(self) -> list[ProgramaSocial]:
        return await self.programa_repo.list_all()

    async def ativar_programa(self, programa_id: UUID) -> ProgramaSocial:
        item = await self.buscar_programa(programa_id)
        item.ativar()
        return await self.programa_repo.save(item)

    async def suspender_programa(self, programa_id: UUID, motivo: str | None=None) -> ProgramaSocial:
        item = await self.buscar_programa(programa_id)
        item.suspender(motivo)
        return await self.programa_repo.save(item)

    async def encerrar_programa(self, programa_id: UUID, *, data_fim: date, motivo: str | None=None) -> ProgramaSocial:
        item = await self.buscar_programa(programa_id)
        item.encerrar(data_fim, motivo)
        return await self.programa_repo.save(item)

    async def remover_programa(self, programa_id: UUID) -> None:
        if not await self.programa_repo.delete(programa_id):
            raise ValueError('Programa social nao encontrado')