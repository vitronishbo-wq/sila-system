from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.habite_se_repository_port import HabiteSeRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusHabiteSe, TipoHabiteSe
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.habite_se import HabiteSe
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import HabiteSeAlreadyExistsError, HabiteSeNotFoundError

class HabiteSeService:

    def __init__(self, *, habite_se_repo: HabiteSeRepositoryPort) -> None:
        self._habite_se_repo = habite_se_repo

    async def criar(self, *, numero_processo: str, tipo: TipoHabiteSe, alvara_id: UUID, requerente_id: UUID, provincia: str, municipio: str | None=None, endereco_imovel: str | None=None, area_vistoriada: Decimal | None=None, codigo_habite_se: str | None=None) -> HabiteSe:
        codigo = codigo_habite_se or await self._habite_se_repo.next_codigo()
        existente = await self._habite_se_repo.get_by_codigo(codigo)
        if existente:
            raise HabiteSeAlreadyExistsError('Ja existe habite-se com este codigo')
        item = HabiteSe.criar(codigo_habite_se=codigo, numero_processo=numero_processo, tipo=tipo, alvara_id=alvara_id, requerente_id=requerente_id, provincia=provincia, municipio=municipio, endereco_imovel=endereco_imovel, area_vistoriada=area_vistoriada)
        return await self._habite_se_repo.save(item)

    async def agendar_vistoria(self, codigo_habite_se: str, *, data_vistoria: date, tecnico_vistoriador_id: UUID) -> HabiteSe:
        item = await self._obter_ou_erro(codigo_habite_se)
        item.agendar_vistoria(data_vistoria=data_vistoria, tecnico_vistoriador_id=tecnico_vistoriador_id)
        return await self._habite_se_repo.save(item)

    async def aprovar_vistoria(self, codigo_habite_se: str) -> HabiteSe:
        item = await self._obter_ou_erro(codigo_habite_se)
        item.aprovar_vistoria()
        return await self._habite_se_repo.save(item)

    async def reprovar_vistoria(self, codigo_habite_se: str, *, motivo: str) -> HabiteSe:
        item = await self._obter_ou_erro(codigo_habite_se)
        item.reprovar_vistoria(motivo=motivo)
        return await self._habite_se_repo.save(item)

    async def emitir(self, codigo_habite_se: str, *, data_emissao: date, data_validade: date | None=None) -> HabiteSe:
        item = await self._obter_ou_erro(codigo_habite_se)
        item.emitir(data_emissao=data_emissao, data_validade=data_validade)
        return await self._habite_se_repo.save(item)

    async def cancelar(self, codigo_habite_se: str, *, motivo: str) -> HabiteSe:
        item = await self._obter_ou_erro(codigo_habite_se)
        item.cancelar(motivo=motivo)
        return await self._habite_se_repo.save(item)

    async def obter_por_codigo(self, codigo_habite_se: str) -> HabiteSe:
        return await self._obter_ou_erro(codigo_habite_se)

    async def listar(self, *, status: StatusHabiteSe | None=None, tipo: TipoHabiteSe | None=None, provincia: str | None=None) -> list[HabiteSe]:
        return await self._habite_se_repo.list(status=status, tipo=tipo, provincia=provincia)

    async def _obter_ou_erro(self, codigo_habite_se: str) -> HabiteSe:
        item = await self._habite_se_repo.get_by_codigo(codigo_habite_se)
        if not item:
            raise HabiteSeNotFoundError('Habite-se nao encontrado')
        return item