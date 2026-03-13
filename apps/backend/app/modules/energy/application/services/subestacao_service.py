from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import SubestacaoRepositoryPort
from apps.backend.app.modules.energy.domain.enums import ClasseTensao, StatusInfraEnergia
from apps.backend.app.modules.energy.domain.models import Subestacao
from apps.backend.app.modules.energy.core.exceptions import InvalidSubestacaoStateError, SubestacaoNotFoundError

class SubestacaoService:

    def __init__(self, *, repository: SubestacaoRepositoryPort) -> None:
        self._repository = repository

    async def cadastrar(self, *, nome: str, tensao_nominal_kv: Decimal, classe_tensao: ClasseTensao, municipio: str, provincia: str) -> Subestacao:
        item = Subestacao.cadastrar(nome=nome, tensao_nominal_kv=tensao_nominal_kv, classe_tensao=classe_tensao, municipio=municipio, provincia=provincia)
        return await self._repository.save(item)

    async def iniciar_construcao(self, id: UUID, *, data_inicio: date) -> Subestacao:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_construcao(data_inicio)
        except ValueError as exc:
            raise InvalidSubestacaoStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def iniciar_operacao(self, id: UUID, *, data_operacao: date) -> Subestacao:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_operacao(data_operacao)
        except ValueError as exc:
            raise InvalidSubestacaoStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def listar(self, *, status: StatusInfraEnergia | None=None) -> list[Subestacao]:
        return await self._repository.list(status=status)

    async def _obter_ou_erro(self, id: UUID) -> Subestacao:
        item = await self._repository.get_by_id(id)
        if not item:
            raise SubestacaoNotFoundError('Subestacao nao encontrada')
        return item
