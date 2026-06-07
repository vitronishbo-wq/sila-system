from __future__ import annotations

from apps.backend.app.modules.resources.ambiente.application.ports import (
    CondicionanteRepositoryPort,
    LicencaRepositoryPort,
)
from apps.backend.app.modules.resources.ambiente.domain.enums import (
    StatusCondicionante,
    StatusLicenca,
)
from apps.backend.app.modules.resources.ambiente.domain.models.condicionante import Condicionante
from apps.backend.app.modules.resources.ambiente.exceptions import (
    CondicionanteNotFoundError,
    LicencaNotFoundError,
)


class CondicionanteService:
    def __init__(
        self,
        *,
        licenca_repo: LicencaRepositoryPort,
        condicionante_repo: CondicionanteRepositoryPort,
    ) -> None:
        self._licenca_repo = licenca_repo
        self._condicionante_repo = condicionante_repo

    async def criar(self, *, numero_licenca: str, descricao: str, prazo_dias: int) -> Condicionante:
        licenca = await self._licenca_repo.get_by_numero(numero_licenca)
        if not licenca:
            raise LicencaNotFoundError("Licenca ambiental nao encontrada")
        if licenca.status != StatusLicenca.DEFERIDA:
            raise ValueError("Licenca precisa estar deferida para receber condicionante")
        item = Condicionante.criar(
            numero_licenca=numero_licenca, descricao=descricao, prazo_dias=prazo_dias
        )
        item.codigo_condicionante = await self._condicionante_repo.next_codigo()
        return await self._condicionante_repo.save(item)

    async def iniciar_cumprimento(self, codigo_condicionante: str) -> Condicionante:
        item = await self._condicionante_repo.get_by_codigo(codigo_condicionante)
        if not item:
            raise CondicionanteNotFoundError("Condicionante nao encontrada")
        item.iniciar_cumprimento()
        return await self._condicionante_repo.save(item)

    async def registrar_cumprimento(
        self, codigo_condicionante: str, evidencia: str | None = None
    ) -> Condicionante:
        item = await self._condicionante_repo.get_by_codigo(codigo_condicionante)
        if not item:
            raise CondicionanteNotFoundError("Condicionante nao encontrada")
        item.registrar_cumprimento(evidencia)
        return await self._condicionante_repo.save(item)

    async def marcar_descumprimento(self, codigo_condicionante: str, motivo: str) -> Condicionante:
        item = await self._condicionante_repo.get_by_codigo(codigo_condicionante)
        if not item:
            raise CondicionanteNotFoundError("Condicionante nao encontrada")
        item.marcar_descumprimento(motivo)
        return await self._condicionante_repo.save(item)

    async def obter_por_codigo(self, codigo_condicionante: str) -> Condicionante:
        item = await self._condicionante_repo.get_by_codigo(codigo_condicionante)
        if not item:
            raise CondicionanteNotFoundError("Condicionante nao encontrada")
        return item

    async def listar(
        self, *, numero_licenca: str | None = None, status: StatusCondicionante | None = None
    ) -> list[Condicionante]:
        return await self._condicionante_repo.list(numero_licenca=numero_licenca, status=status)
