from __future__ import annotations

from apps.backend.app.modules.resources.pescas.application.ports import (
    CitizenServicePort,
    PescadorRepositoryPort,
    RequestServicePort,
)
from apps.backend.app.modules.resources.pescas.domain.enums import TipoPescador
from apps.backend.app.modules.resources.pescas.domain.models.pescador import Pescador


class PescadorService:
    def __init__(
        self,
        pescador_repo: PescadorRepositoryPort,
        citizen_service: CitizenServicePort,
        request_service: RequestServicePort,
    ):
        self.pescador_repo = pescador_repo
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def cadastrar_pescador(
        self, *, nome: str, tipo: TipoPescador, citizen_id, numero_registro: str | None = None
    ) -> Pescador:
        if not await self.citizen_service.is_citizen_active(citizen_id):
            raise ValueError("Cidadao nao encontrado ou inativo")
        registro = numero_registro or await self.pescador_repo.next_registro()
        if await self.pescador_repo.get_by_numero_registro(registro):
            raise ValueError("Numero de registro ja cadastrado")
        item = Pescador.cadastrar(
            nome=nome, numero_registro=registro, tipo=tipo, citizen_id=citizen_id
        )
        saved = await self.pescador_repo.save(item)
        await self.request_service.create_request(
            request_type="CADASTRO_PESCADOR",
            entity_id=saved.id,
            citizen_id=citizen_id,
            numero_processo=registro,
            metadata={"tipo": tipo.value, "nome": nome},
        )
        return saved

    async def buscar_pescador(self, pescador_id) -> Pescador:
        item = await self.pescador_repo.get_by_id(pescador_id)
        if not item:
            raise ValueError("Pescador nao encontrado")
        return item

    async def listar_pescadores(self, *, tipo: TipoPescador | None = None) -> list[Pescador]:
        return await self.pescador_repo.list_by_tipo(tipo)
