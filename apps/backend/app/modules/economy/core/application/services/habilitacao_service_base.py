from __future__ import annotations
from datetime import date
from typing import Generic, TypeVar
from uuid import UUID
from ....trade.external.application.ports import HabilitacaoRepositoryPortBase
from ....trade.external.domain.enums import StatusHabilitacao, TipoPessoa
from ....trade.external.domain.models import HabilitacaoBase
THabilitacao = TypeVar('THabilitacao', bound=HabilitacaoBase)

class HabilitacaoServiceBase(Generic[THabilitacao]):

    def __init__(self, *, repository: HabilitacaoRepositoryPortBase[THabilitacao], domain_cls: type[THabilitacao], not_found_error_cls: type[Exception], already_exists_error_cls: type[Exception], invalid_state_error_cls: type[Exception], entity_label: str) -> None:
        self._repository = repository
        self._domain_cls = domain_cls
        self._not_found_error_cls = not_found_error_cls
        self._already_exists_error_cls = already_exists_error_cls
        self._invalid_state_error_cls = invalid_state_error_cls
        self._entity_label = entity_label

    async def solicitar(self, *, tipo_pessoa: TipoPessoa, razao_social: str, cnpj_cpf: str, numero_processo: str, data_solicitacao: date) -> THabilitacao:
        existente = await self._repository.get_by_numero_processo(numero_processo)
        if existente:
            raise self._already_exists_error_cls(f'{self._entity_label} ja cadastrada para o numero de processo informado')
        item = self._domain_cls.solicitar(tipo_pessoa=tipo_pessoa, razao_social=razao_social, cnpj_cpf=cnpj_cpf, numero_processo=numero_processo, data_solicitacao=data_solicitacao)
        return await self._repository.save(item)

    async def aprovar(self, id: UUID, *, numero_radar: str, data_analise: date, data_validade: date) -> THabilitacao:
        item = await self._obter_ou_erro(id)
        try:
            item.aprovar(numero_radar=numero_radar, data_analise=data_analise, data_validade=data_validade)
        except ValueError as exc:
            raise self._invalid_state_error_cls(str(exc)) from exc
        return await self._repository.save(item)

    async def rejeitar(self, id: UUID, *, data_analise: date, motivo: str) -> THabilitacao:
        item = await self._obter_ou_erro(id)
        try:
            item.rejeitar(data_analise=data_analise, motivo=motivo)
        except ValueError as exc:
            raise self._invalid_state_error_cls(str(exc)) from exc
        return await self._repository.save(item)

    async def reabrir(self, id: UUID) -> THabilitacao:
        item = await self._obter_ou_erro(id)
        try:
            item.reabrir()
        except ValueError as exc:
            raise self._invalid_state_error_cls(str(exc)) from exc
        return await self._repository.save(item)

    async def obter_por_id(self, id: UUID) -> THabilitacao:
        return await self._obter_ou_erro(id)

    async def listar(self, *, status: StatusHabilitacao | None=None) -> list[THabilitacao]:
        return await self._repository.list(status=status)

    async def _obter_ou_erro(self, id: UUID) -> THabilitacao:
        item = await self._repository.get_by_id(id)
        if not item:
            raise self._not_found_error_cls(f'{self._entity_label} nao encontrada')
        return item