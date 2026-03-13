from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.alvara_repository_port import AlvaraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusAlvara, TipoAlvara
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.alvara import Alvara
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import AlvaraAlreadyExistsError, AlvaraNotFoundError

class AlvaraService:

    def __init__(self, *, alvara_repo: AlvaraRepositoryPort) -> None:
        self._alvara_repo = alvara_repo

    async def criar(self, *, numero_processo: str, tipo: TipoAlvara, licenca_urbanistica_id: UUID, requerente_id: UUID, provincia: str, municipio: str | None=None, endereco_obra: str | None=None, area_autorizada: Decimal | None=None, codigo_alvara: str | None=None) -> Alvara:
        codigo = codigo_alvara or await self._alvara_repo.next_codigo()
        existente = await self._alvara_repo.get_by_codigo(codigo)
        if existente:
            raise AlvaraAlreadyExistsError('Ja existe alvara com este codigo')
        item = Alvara.criar(codigo_alvara=codigo, numero_processo=numero_processo, tipo=tipo, licenca_urbanistica_id=licenca_urbanistica_id, requerente_id=requerente_id, provincia=provincia, municipio=municipio, endereco_obra=endereco_obra, area_autorizada=area_autorizada)
        return await self._alvara_repo.save(item)

    async def iniciar_analise(self, codigo_alvara: str) -> Alvara:
        item = await self._obter_ou_erro(codigo_alvara)
        item.iniciar_analise()
        return await self._alvara_repo.save(item)

    async def solicitar_pendencia(self, codigo_alvara: str, *, motivo: str) -> Alvara:
        item = await self._obter_ou_erro(codigo_alvara)
        item.solicitar_pendencia(motivo=motivo)
        return await self._alvara_repo.save(item)

    async def deferir(self, codigo_alvara: str, *, data_emissao: date, data_validade: date, analista_id: UUID) -> Alvara:
        item = await self._obter_ou_erro(codigo_alvara)
        item.deferir(data_emissao=data_emissao, data_validade=data_validade, analista_id=analista_id)
        return await self._alvara_repo.save(item)

    async def indeferir(self, codigo_alvara: str, *, motivo: str) -> Alvara:
        item = await self._obter_ou_erro(codigo_alvara)
        item.indeferir(motivo=motivo)
        return await self._alvara_repo.save(item)

    async def cancelar(self, codigo_alvara: str, *, motivo: str) -> Alvara:
        item = await self._obter_ou_erro(codigo_alvara)
        item.cancelar(motivo=motivo)
        return await self._alvara_repo.save(item)

    async def obter_por_codigo(self, codigo_alvara: str) -> Alvara:
        return await self._obter_ou_erro(codigo_alvara)

    async def listar(self, *, status: StatusAlvara | None=None, tipo: TipoAlvara | None=None, provincia: str | None=None) -> list[Alvara]:
        return await self._alvara_repo.list(status=status, tipo=tipo, provincia=provincia)

    async def _obter_ou_erro(self, codigo_alvara: str) -> Alvara:
        item = await self._alvara_repo.get_by_codigo(codigo_alvara)
        if not item:
            raise AlvaraNotFoundError('Alvara nao encontrado')
        return item