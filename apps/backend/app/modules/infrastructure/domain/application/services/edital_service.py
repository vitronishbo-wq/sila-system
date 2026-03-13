from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.infrastructure.application.ports.edital_repository_port import EditalRepositoryPort
from apps.backend.app.modules.infrastructure.domain.enums import StatusEdital
from apps.backend.app.modules.infrastructure.domain.models.edital import Edital
from apps.backend.app.modules.infrastructure.core.exceptions import EditalAlreadyExistsError, EditalNotFoundError

class EditalService:

    def __init__(self, *, edital_repo: EditalRepositoryPort) -> None:
        self._edital_repo = edital_repo

    async def publicar(self, *, titulo: str, objeto: str, licitacao_id: UUID, data_publicacao: date, data_abertura: date, data_encerramento: date, numero_edital: str | None=None) -> Edital:
        numero = numero_edital or await self._edital_repo.next_numero()
        existente = await self._edital_repo.get_by_numero(numero)
        if existente:
            raise EditalAlreadyExistsError('Ja existe edital com este numero')
        item = Edital.publicar(numero_edital=numero, titulo=titulo, objeto=objeto, licitacao_id=licitacao_id, data_publicacao=data_publicacao, data_abertura=data_abertura, data_encerramento=data_encerramento)
        return await self._edital_repo.save(item)

    async def impugnar(self, numero_edital: str, *, motivo: str) -> Edital:
        item = await self._obter_ou_erro(numero_edital)
        item.impugnar(motivo)
        return await self._edital_repo.save(item)

    async def retificar(self, numero_edital: str, *, descricao: str) -> Edital:
        item = await self._obter_ou_erro(numero_edital)
        item.retificar(descricao)
        return await self._edital_repo.save(item)

    async def suspender(self, numero_edital: str, *, motivo: str) -> Edital:
        item = await self._obter_ou_erro(numero_edital)
        item.suspender(motivo)
        return await self._edital_repo.save(item)

    async def revogar(self, numero_edital: str, *, motivo: str) -> Edital:
        item = await self._obter_ou_erro(numero_edital)
        item.revogar(motivo)
        return await self._edital_repo.save(item)

    async def encerrar(self, numero_edital: str, *, data_encerramento: date | None=None) -> Edital:
        item = await self._obter_ou_erro(numero_edital)
        item.encerrar(data_encerramento=data_encerramento)
        return await self._edital_repo.save(item)

    async def obter_por_numero(self, numero_edital: str) -> Edital:
        return await self._obter_ou_erro(numero_edital)

    async def listar(self, *, status: StatusEdital | None=None, licitacao_id: UUID | None=None) -> list[Edital]:
        return await self._edital_repo.list(status=status, licitacao_id=licitacao_id)

    async def _obter_ou_erro(self, numero_edital: str) -> Edital:
        item = await self._edital_repo.get_by_numero(numero_edital)
        if not item:
            raise EditalNotFoundError('Edital nao encontrado')
        return item
