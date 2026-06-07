from __future__ import annotations

from uuid import UUID

from apps.backend.app.modules.society.desporto.application.events import (
    EstadioCadastradoEvent,
    EventBus,
)
from apps.backend.app.modules.society.desporto.application.ports.estadio_repository_port import (
    EstadioRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.obras_publicas_service_port import (
    ObrasPublicasServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.outbox_repository_port import (
    OutboxRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.desporto.domain.enums import EstadoRelvado, TipoEstadio
from apps.backend.app.modules.society.desporto.domain.models.estadio import Estadio


class EstadioService:
    def __init__(
        self,
        *,
        estadio_repo: EstadioRepositoryPort,
        obras_publicas_service: ObrasPublicasServicePort | None = None,
        request_service: RequestServicePort | None = None,
        event_bus: EventBus | None = None,
        outbox_repo: OutboxRepositoryPort | None = None,
    ) -> None:
        self.estadio_repo = estadio_repo
        self.obras_publicas_service = obras_publicas_service
        self.request_service = request_service
        self.event_bus = event_bus
        self.outbox_repo = outbox_repo

    async def cadastrar_estadio(
        self,
        *,
        nome: str,
        tipo: TipoEstadio,
        municipio: str,
        provincia: str,
        capacidade: int,
        estado_relvado: EstadoRelvado,
        codigo_obra_instalacao: str | None = None,
        clube_mandante_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Estadio:
        if codigo_obra_instalacao and self.obras_publicas_service is not None:
            obra_ok = await self.obras_publicas_service.obra_exists(codigo_obra_instalacao)
            if not obra_ok:
                raise ValueError("Obra de instalacao informada nao encontrada")
        codigo = await self.estadio_repo.next_codigo()
        estadio = Estadio.cadastrar(
            codigo_estadio=codigo,
            nome=nome,
            tipo=tipo,
            municipio=municipio,
            provincia=provincia,
            capacidade=capacidade,
            estado_relvado=estado_relvado,
            codigo_obra_instalacao=codigo_obra_instalacao,
            clube_mandante_id=clube_mandante_id,
            observacoes=observacoes,
        )
        saved = await self.estadio_repo.save(estadio)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_ESTADIO",
                entity_id=saved.id,
                metadata={
                    "codigo_estadio": saved.codigo_estadio,
                    "nome": saved.nome,
                    "municipio": saved.municipio,
                },
                numero_processo=saved.codigo_estadio,
            )
        event = EstadioCadastradoEvent(
            estadio_id=saved.id,
            codigo_estadio=saved.codigo_estadio,
            nome=saved.nome,
            municipio=saved.municipio,
            provincia=saved.provincia,
        )
        if self.outbox_repo is not None:
            await self.outbox_repo.append(event)
        if self.event_bus is not None:
            await self.event_bus.publish(event)
        return saved

    async def buscar_estadio(self, estadio_id: UUID) -> Estadio:
        item = await self.estadio_repo.get_by_id(estadio_id)
        if item is None:
            raise ValueError("Estadio nao encontrado")
        return item

    async def listar_estadios(
        self, *, municipio: str | None = None, somente_ativos: bool = True
    ) -> list[Estadio]:
        if municipio is not None:
            items = await self.estadio_repo.list_by_municipio(municipio)
        else:
            items = await self.estadio_repo.list_all()
        if somente_ativos:
            return [item for item in items if item.ativo]
        return items

    async def atualizar_estadio(
        self,
        *,
        estadio_id: UUID,
        nome: str | None = None,
        tipo: TipoEstadio | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        capacidade: int | None = None,
        estado_relvado: EstadoRelvado | None = None,
        codigo_obra_instalacao: str | None = None,
        clube_mandante_id: UUID | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> Estadio:
        item = await self.buscar_estadio(estadio_id)
        if codigo_obra_instalacao and self.obras_publicas_service is not None:
            obra_ok = await self.obras_publicas_service.obra_exists(codigo_obra_instalacao)
            if not obra_ok:
                raise ValueError("Obra de instalacao informada nao encontrada")
        item.atualizar(
            nome=nome,
            tipo=tipo,
            municipio=municipio,
            provincia=provincia,
            capacidade=capacidade,
            estado_relvado=estado_relvado,
            codigo_obra_instalacao=codigo_obra_instalacao,
            clube_mandante_id=clube_mandante_id,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.estadio_repo.save(item)

    async def remover_estadio(self, estadio_id: UUID) -> None:
        deleted = await self.estadio_repo.delete(estadio_id)
        if not deleted:
            raise ValueError("Estadio nao encontrado")
