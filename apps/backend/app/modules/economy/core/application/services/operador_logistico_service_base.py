from __future__ import annotations

from datetime import date
from typing import Generic, TypeVar
from uuid import UUID

from ....trade.external.application.ports import OperadorLogisticoRepositoryPort
from ....trade.external.domain.enums import StatusHabilitacao, TipoPessoa
from ....trade.external.domain.models import OperadorLogisticoBase

TOperadorLogistico = TypeVar("TOperadorLogistico", bound=OperadorLogisticoBase)


class OperadorLogisticoServiceBase(Generic[TOperadorLogistico]):
    def __init__(
        self,
        *,
        repository: OperadorLogisticoRepositoryPort[TOperadorLogistico],
        domain_cls: type[TOperadorLogistico],
        not_found_error_cls: type[Exception],
        already_exists_error_cls: type[Exception],
        invalid_state_error_cls: type[Exception],
        entity_label: str,
    ) -> None:
        self._repository = repository
        self._domain_cls = domain_cls
        self._not_found_error_cls = not_found_error_cls
        self._already_exists_error_cls = already_exists_error_cls
        self._invalid_state_error_cls = invalid_state_error_cls
        self._entity_label = entity_label

    async def cadastrar(
        self,
        *,
        razao_social: str,
        cnpj_cpf: str,
        tipo_pessoa: TipoPessoa,
        endereco: str,
        numero: str,
        bairro: str,
        municipio: str,
        provincia: str,
        cep: str,
    ) -> TOperadorLogistico:
        existente = await self._repository.get_by_cnpj_cpf(cnpj_cpf)
        if existente:
            raise self._already_exists_error_cls(
                f"{self._entity_label} ja cadastrado para o CNPJ/CPF informado"
            )
        item = self._domain_cls.cadastrar(
            razao_social=razao_social,
            cnpj_cpf=cnpj_cpf,
            tipo_pessoa=tipo_pessoa,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            municipio=municipio,
            provincia=provincia,
            cep=cep,
        )
        return await self._repository.save(item)

    async def habilitar(
        self, id: UUID, *, numero_radar: str, data_habilitacao: date, data_validade: date
    ) -> TOperadorLogistico:
        item = await self._obter_ou_erro(id)
        try:
            item.habilitar(numero_radar, data_habilitacao, data_validade)
        except ValueError as exc:
            raise self._invalid_state_error_cls(str(exc)) from exc
        return await self._repository.save(item)

    async def suspender(self, id: UUID, *, data_suspensao: date, motivo: str) -> TOperadorLogistico:
        item = await self._obter_ou_erro(id)
        try:
            item.suspender(data_suspensao, motivo)
        except ValueError as exc:
            raise self._invalid_state_error_cls(str(exc)) from exc
        return await self._repository.save(item)

    async def cancelar(
        self, id: UUID, *, data_cancelamento: date, motivo: str
    ) -> TOperadorLogistico:
        item = await self._obter_ou_erro(id)
        try:
            item.cancelar(data_cancelamento, motivo)
        except ValueError as exc:
            raise self._invalid_state_error_cls(str(exc)) from exc
        return await self._repository.save(item)

    async def reabilitar(self, id: UUID) -> TOperadorLogistico:
        item = await self._obter_ou_erro(id)
        try:
            item.reabilitar()
        except ValueError as exc:
            raise self._invalid_state_error_cls(str(exc)) from exc
        return await self._repository.save(item)

    async def obter_por_id(self, id: UUID) -> TOperadorLogistico:
        return await self._obter_ou_erro(id)

    async def listar(
        self, *, status: StatusHabilitacao | None = None, municipio: str | None = None
    ) -> list[TOperadorLogistico]:
        return await self._repository.list(status=status, municipio=municipio)

    async def _obter_ou_erro(self, id: UUID) -> TOperadorLogistico:
        item = await self._repository.get_by_id(id)
        if not item:
            raise self._not_found_error_cls(f"{self._entity_label} nao encontrado")
        return item
