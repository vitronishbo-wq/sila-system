from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.society.cultura.application.events import (
    ArtistaRegistradoEvent,
    event_bus,
)
from apps.backend.app.modules.society.cultura.application.ports.artista_repository_port import (
    ArtistaRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.cultura.domain.enums import TipoArtista
from apps.backend.app.modules.society.cultura.domain.models.artista import Artista


class ArtistaService:
    def __init__(
        self,
        *,
        artista_repo: ArtistaRepositoryPort,
        citizen_service: CitizenServicePort | None = None,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.artista_repo = artista_repo
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def cadastrar_artista(
        self,
        *,
        nome: str,
        tipo: list[TipoArtista],
        citizen_id: UUID | None = None,
        nome_artistico: str | None = None,
        data_nascimento: date | None = None,
        naturalidade: str | None = None,
        nacionalidade: str = "Angolana",
        biografia: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        observacoes: str | None = None,
    ) -> Artista:
        if citizen_id is not None and self.citizen_service is not None:
            ativo = await self.citizen_service.is_citizen_active(citizen_id)
            if not ativo:
                raise ValueError("Cidadao nao encontrado ou inativo")
        registro = await self.artista_repo.next_registro()
        artista = Artista.cadastrar(
            nome=nome,
            tipo=tipo,
            registro=registro,
            citizen_id=citizen_id,
            nome_artistico=nome_artistico,
            data_nascimento=data_nascimento,
            naturalidade=naturalidade,
            nacionalidade=nacionalidade,
            biografia=biografia,
            municipio=municipio,
            provincia=provincia,
            observacoes=observacoes,
        )
        saved = await self.artista_repo.save(artista)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_ARTISTA",
                entity_id=saved.id,
                citizen_id=citizen_id,
                metadata={
                    "registro_cultural": saved.registro_cultural,
                    "nome": saved.nome,
                    "tipo": [item.value for item in saved.tipo],
                },
                numero_processo=saved.registro_cultural,
            )
        await event_bus.publish(
            ArtistaRegistradoEvent(
                artista_id=saved.id,
                nome=saved.nome,
                cpf=str(saved.citizen_id or ""),
                tipo=",".join(item.value for item in saved.tipo),
            )
        )
        return saved

    async def buscar_artista(self, artista_id: UUID) -> Artista:
        item = await self.artista_repo.get_by_id(artista_id)
        if item is None:
            raise ValueError("Artista nao encontrado")
        return item

    async def listar_artistas(
        self, *, tipo: TipoArtista | None = None, somente_ativos: bool = True
    ) -> list[Artista]:
        if tipo is not None:
            itens = await self.artista_repo.list_by_tipo(tipo)
        else:
            itens = await self.artista_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_artista(
        self,
        *,
        artista_id: UUID,
        nome: str | None = None,
        tipo: list[TipoArtista] | None = None,
        nome_artistico: str | None = None,
        data_nascimento: date | None = None,
        naturalidade: str | None = None,
        nacionalidade: str | None = None,
        biografia: str | None = None,
        municipio: str | None = None,
        provincia: str | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> Artista:
        item = await self.buscar_artista(artista_id)
        item.atualizar(
            nome=nome,
            tipo=tipo,
            nome_artistico=nome_artistico,
            data_nascimento=data_nascimento,
            naturalidade=naturalidade,
            nacionalidade=nacionalidade,
            biografia=biografia,
            municipio=municipio,
            provincia=provincia,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.artista_repo.save(item)

    async def remover_artista(self, artista_id: UUID) -> None:
        deleted = await self.artista_repo.delete(artista_id)
        if not deleted:
            raise ValueError("Artista nao encontrado")
