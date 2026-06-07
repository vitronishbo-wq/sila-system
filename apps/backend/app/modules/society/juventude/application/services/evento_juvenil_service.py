from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.society.juventude.application.ports.evento_juvenil_repository_port import (
    EventoJuvenilRepositoryPort,
)
from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import (
    JovemRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    AreaInteresse,
    StatusEvento,
    TipoEvento,
)
from apps.backend.app.modules.society.juventude.domain.models.evento_juvenil import EventoJuvenil


class EventoJuvenilService:
    def __init__(
        self, *, evento_repo: EventoJuvenilRepositoryPort, jovem_repo: JovemRepositoryPort
    ) -> None:
        self.evento_repo = evento_repo
        self.jovem_repo = jovem_repo

    async def criar_evento(
        self,
        *,
        titulo: str,
        tipo_evento: TipoEvento,
        area_interesse: AreaInteresse,
        data_evento: date,
        local: str,
        municipio: str,
        provincia: str,
        vagas: int | None = None,
        observacoes: str | None = None,
    ) -> EventoJuvenil:
        codigo = await self.evento_repo.next_codigo()
        item = EventoJuvenil.criar(
            codigo_evento=codigo,
            titulo=titulo,
            tipo_evento=tipo_evento,
            area_interesse=area_interesse,
            data_evento=data_evento,
            local=local,
            municipio=municipio,
            provincia=provincia,
            vagas=vagas,
            observacoes=observacoes,
        )
        return await self.evento_repo.save(item)

    async def buscar_evento(self, evento_id: UUID) -> EventoJuvenil:
        item = await self.evento_repo.get_by_id(evento_id)
        if item is None:
            raise ValueError("Evento nao encontrado")
        return item

    async def listar_eventos(self, *, status: StatusEvento | None = None) -> list[EventoJuvenil]:
        if status is not None:
            return await self.evento_repo.list_by_status(status)
        return await self.evento_repo.list_all()

    async def abrir_inscricoes(self, evento_id: UUID) -> EventoJuvenil:
        item = await self.buscar_evento(evento_id)
        item.abrir_inscricoes()
        return await self.evento_repo.save(item)

    async def inscrever_jovem(self, *, evento_id: UUID, jovem_id: UUID) -> EventoJuvenil:
        if await self.jovem_repo.get_by_id(jovem_id) is None:
            raise ValueError("Jovem nao encontrado para inscricao no evento")
        item = await self.buscar_evento(evento_id)
        item.registrar_participante(jovem_id)
        return await self.evento_repo.save(item)

    async def concluir_evento(self, evento_id: UUID) -> EventoJuvenil:
        item = await self.buscar_evento(evento_id)
        item.concluir()
        return await self.evento_repo.save(item)

    async def remover_evento(self, evento_id: UUID) -> None:
        if not await self.evento_repo.delete(evento_id):
            raise ValueError("Evento nao encontrado")
