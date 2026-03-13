from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import LinhaTransmissaoRepositoryPort
from apps.backend.app.modules.energy.domain.enums import StatusInfraEnergia
from apps.backend.app.modules.energy.domain.models import LinhaTransmissao
from apps.backend.app.modules.energy.domain.exceptions import InvalidLinhaTransmissaoStateError, LinhaTransmissaoNotFoundError

class LinhaTransmissaoService:

    def __init__(self, *, repository: LinhaTransmissaoRepositoryPort) -> None:
        self._repository = repository

    async def cadastrar(self, *, origem_id: UUID, origem_tipo: str, destino_id: UUID, destino_tipo: str, capacidade_mw: Decimal, extensao_km: Decimal) -> LinhaTransmissao:
        item = LinhaTransmissao.cadastrar(origem_id=origem_id, origem_tipo=origem_tipo, destino_id=destino_id, destino_tipo=destino_tipo, capacidade_mw=capacidade_mw, extensao_km=extensao_km)
        return await self._repository.save(item)

    async def iniciar_construcao(self, id: UUID, *, data_inicio: date) -> LinhaTransmissao:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_construcao(data_inicio)
        except ValueError as exc:
            raise InvalidLinhaTransmissaoStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def iniciar_operacao(self, id: UUID, *, data_operacao: date) -> LinhaTransmissao:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_operacao(data_operacao)
        except ValueError as exc:
            raise InvalidLinhaTransmissaoStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def listar(self, *, status: StatusInfraEnergia | None=None) -> list[LinhaTransmissao]:
        return await self._repository.list(status=status)

    async def _obter_ou_erro(self, id: UUID) -> LinhaTransmissao:
        item = await self._repository.get_by_id(id)
        if not item:
            raise LinhaTransmissaoNotFoundError('Linha de transmissao nao encontrada')
        return item
