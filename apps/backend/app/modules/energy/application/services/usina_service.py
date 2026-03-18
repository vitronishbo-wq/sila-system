from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.energy.application.ports import UsinaRepositoryPort
from apps.backend.app.modules.energy.domain.enums import FonteEnergia, StatusUsina, TipoUsina
from apps.backend.app.modules.energy.domain.models import Usina
from apps.backend.app.modules.energy.domain.exceptions import InvalidUsinaStateError, UsinaAlreadyExistsError, UsinaNotFoundError

class UsinaService:

    def __init__(self, *, usina_repo: UsinaRepositoryPort) -> None:
        self._usina_repo = usina_repo

    async def cadastrar_usina(self, *, codigo_aneel: str, nome: str, fonte: FonteEnergia, tipo: TipoUsina, potencia_instalada_mw: Decimal, proprietario_id: UUID, proprietario_tipo: str, municipio: str, provincia: str) -> Usina:
        existente = await self._usina_repo.get_by_codigo_aneel(codigo_aneel)
        if existente:
            raise UsinaAlreadyExistsError('Ja existe usina para o codigo ANEEL informado')
        usina = Usina.cadastrar(codigo_aneel=codigo_aneel, nome=nome, fonte=fonte, tipo=tipo, potencia_instalada_mw=potencia_instalada_mw, proprietario_id=proprietario_id, proprietario_tipo=proprietario_tipo, municipio=municipio, provincia=provincia)
        return await self._usina_repo.save(usina)

    async def iniciar_construcao(self, usina_id: UUID, *, data_inicio: date) -> Usina:
        usina = await self._obter_ou_erro(usina_id)
        try:
            usina.iniciar_construcao(data_inicio)
        except ValueError as exc:
            raise InvalidUsinaStateError(str(exc)) from exc
        return await self._usina_repo.save(usina)

    async def iniciar_operacao(self, usina_id: UUID, *, data_operacao: date) -> Usina:
        usina = await self._obter_ou_erro(usina_id)
        try:
            usina.iniciar_operacao(data_operacao)
        except ValueError as exc:
            raise InvalidUsinaStateError(str(exc)) from exc
        return await self._usina_repo.save(usina)

    async def paralisar_usina(self, usina_id: UUID, *, motivo: str) -> Usina:
        usina = await self._obter_ou_erro(usina_id)
        try:
            usina.paralisar(motivo)
        except ValueError as exc:
            raise InvalidUsinaStateError(str(exc)) from exc
        return await self._usina_repo.save(usina)

    async def desativar_usina(self, usina_id: UUID, *, motivo: str) -> Usina:
        usina = await self._obter_ou_erro(usina_id)
        try:
            usina.desativar(motivo)
        except ValueError as exc:
            raise InvalidUsinaStateError(str(exc)) from exc
        return await self._usina_repo.save(usina)

    async def atualizar_potencia_fiscalizada(self, usina_id: UUID, *, potencia: Decimal) -> Usina:
        usina = await self._obter_ou_erro(usina_id)
        try:
            usina.atualizar_potencia_fiscalizada(potencia)
        except ValueError as exc:
            raise InvalidUsinaStateError(str(exc)) from exc
        return await self._usina_repo.save(usina)

    async def obter_por_id(self, usina_id: UUID) -> Usina:
        return await self._obter_ou_erro(usina_id)

    async def listar(self, *, status: StatusUsina | None=None, fonte: FonteEnergia | None=None, provincia: str | None=None) -> list[Usina]:
        return await self._usina_repo.list(status=status, fonte=fonte, provincia=provincia)

    async def _obter_ou_erro(self, usina_id: UUID) -> Usina:
        usina = await self._usina_repo.get_by_id(usina_id)
        if not usina:
            raise UsinaNotFoundError('Usina nao encontrada')
        return usina