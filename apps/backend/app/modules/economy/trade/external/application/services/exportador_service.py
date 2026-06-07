from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.economy.trade.external.application.ports import (
    ExportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.enums import (
    RegimeExportacao,
    StatusHabilitacao,
    TipoPessoa,
)
from apps.backend.app.modules.economy.trade.external.domain.models import Exportador
from apps.backend.app.modules.economy.trade.external.exceptions import (
    ExportadorAlreadyExistsError,
    ExportadorNotFoundError,
    InvalidExportadorStateError,
)


class ExportadorService:
    def __init__(self, *, repository: ExportadorRepositoryPort) -> None:
        self._repository = repository

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
        regimes_autorizados: list[RegimeExportacao],
    ) -> Exportador:
        existente = await self._repository.get_by_cnpj_cpf(cnpj_cpf)
        if existente:
            raise ExportadorAlreadyExistsError("Exportador ja cadastrado para o CNPJ/CPF informado")
        item = Exportador.cadastrar(
            razao_social=razao_social,
            cnpj_cpf=cnpj_cpf,
            tipo_pessoa=tipo_pessoa,
            endereco=endereco,
            numero=numero,
            bairro=bairro,
            municipio=municipio,
            provincia=provincia,
            cep=cep,
            regimes_autorizados=regimes_autorizados,
        )
        return await self._repository.save(item)

    async def habilitar(
        self, id: UUID, *, numero_radar: str, data_habilitacao: date, data_validade: date
    ) -> Exportador:
        item = await self._obter_ou_erro(id)
        try:
            item.habilitar(numero_radar, data_habilitacao, data_validade)
        except ValueError as exc:
            raise InvalidExportadorStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def suspender(self, id: UUID, *, data_suspensao: date, motivo: str) -> Exportador:
        item = await self._obter_ou_erro(id)
        try:
            item.suspender(data_suspensao, motivo)
        except ValueError as exc:
            raise InvalidExportadorStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def cancelar(self, id: UUID, *, data_cancelamento: date, motivo: str) -> Exportador:
        item = await self._obter_ou_erro(id)
        try:
            item.cancelar(data_cancelamento, motivo)
        except ValueError as exc:
            raise InvalidExportadorStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def reabilitar(self, id: UUID) -> Exportador:
        item = await self._obter_ou_erro(id)
        try:
            item.reabilitar()
        except ValueError as exc:
            raise InvalidExportadorStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def adicionar_produto(self, id: UUID, *, produto: str) -> Exportador:
        item = await self._obter_ou_erro(id)
        try:
            item.adicionar_produto(produto)
        except ValueError as exc:
            raise InvalidExportadorStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def adicionar_pais_destino(self, id: UUID, *, pais: str) -> Exportador:
        item = await self._obter_ou_erro(id)
        try:
            item.adicionar_pais_destino(pais)
        except ValueError as exc:
            raise InvalidExportadorStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def obter_por_id(self, id: UUID) -> Exportador:
        return await self._obter_ou_erro(id)

    async def listar(
        self, *, status: StatusHabilitacao | None = None, municipio: str | None = None
    ) -> list[Exportador]:
        return await self._repository.list(status=status, municipio=municipio)

    async def _obter_ou_erro(self, id: UUID) -> Exportador:
        item = await self._repository.get_by_id(id)
        if not item:
            raise ExportadorNotFoundError("Exportador nao encontrado")
        return item
