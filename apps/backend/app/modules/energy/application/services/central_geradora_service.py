from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.energy.application.ports import CentralGeradoraRepositoryPort
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusInfraEnergia
from apps.backend.app.modules.energy.domain.exceptions import (
    CentralGeradoraNotFoundError,
    InvalidCentralGeradoraStateError,
)
from apps.backend.app.modules.energy.domain.models import CentralGeradora


class CentralGeradoraService:
    def __init__(self, *, repository: CentralGeradoraRepositoryPort) -> None:
        self._repository = repository

    async def cadastrar(
        self,
        *,
        nome: str,
        tipo: FonteEnergia,
        capacidade_instalada_mw: Decimal,
        municipio: str,
        provincia: str,
    ) -> CentralGeradora:
        item = CentralGeradora.cadastrar(
            nome=nome,
            tipo=tipo,
            capacidade_instalada_mw=capacidade_instalada_mw,
            municipio=municipio,
            provincia=provincia,
        )
        return await self._repository.save(item)

    async def iniciar_construcao(self, id: UUID, *, data_inicio: date) -> CentralGeradora:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_construcao(data_inicio)
        except ValueError as exc:
            raise InvalidCentralGeradoraStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def iniciar_operacao(self, id: UUID, *, data_operacao: date) -> CentralGeradora:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_operacao(data_operacao)
        except ValueError as exc:
            raise InvalidCentralGeradoraStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def listar(
        self, *, status: StatusInfraEnergia | None = None, tipo: FonteEnergia | None = None
    ) -> list[CentralGeradora]:
        return await self._repository.list(status=status, tipo=tipo)

    async def _obter_ou_erro(self, id: UUID) -> CentralGeradora:
        item = await self._repository.get_by_id(id)
        if not item:
            raise CentralGeradoraNotFoundError("Central geradora nao encontrada")
        return item
