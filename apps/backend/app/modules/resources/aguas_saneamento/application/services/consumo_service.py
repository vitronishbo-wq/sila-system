from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.consumo_repository_port import ConsumoRepositoryPort
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import CategoriaConsumo, StatusConsumo
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.consumo_agua import ConsumoAgua
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import ConsumoAlreadyExistsError, ConsumoNotFoundError

class ConsumoService:

    def __init__(self, *, consumo_repo: ConsumoRepositoryPort) -> None:
        self._consumo_repo = consumo_repo

    async def registrar(self, *, abastecimento_id: UUID, titular_id: UUID, referencia: str, categoria: CategoriaConsumo, volume_m3: Decimal, unidade_volume: str, hidrometro_id: UUID | None=None, leitura_anterior: Decimal | None=None, leitura_atual: Decimal | None=None, data_leitura: date | None=None) -> ConsumoAgua:
        existentes = await self._consumo_repo.list(abastecimento_id=abastecimento_id, titular_id=titular_id, referencia=referencia)
        ativos = {StatusConsumo.REGISTRADO, StatusConsumo.VALIDADO, StatusConsumo.FATURADO}
        if any((item.status in ativos for item in existentes)):
            raise ConsumoAlreadyExistsError('Ja existe consumo registrado para titular e referencia')
        item = ConsumoAgua.registrar(abastecimento_id=abastecimento_id, titular_id=titular_id, referencia=referencia, categoria=categoria, volume_m3=volume_m3, unidade_volume=unidade_volume, hidrometro_id=hidrometro_id, leitura_anterior=leitura_anterior, leitura_atual=leitura_atual, data_leitura=data_leitura)
        item.codigo_consumo = await self._consumo_repo.next_codigo()
        return await self._consumo_repo.save(item)

    async def validar(self, codigo_consumo: str) -> ConsumoAgua:
        item = await self._obter_ou_erro(codigo_consumo)
        item.validar()
        return await self._consumo_repo.save(item)

    async def faturar(self, codigo_consumo: str) -> ConsumoAgua:
        item = await self._obter_ou_erro(codigo_consumo)
        item.faturar()
        return await self._consumo_repo.save(item)

    async def cancelar(self, codigo_consumo: str, *, motivo: str) -> ConsumoAgua:
        item = await self._obter_ou_erro(codigo_consumo)
        item.cancelar(motivo)
        return await self._consumo_repo.save(item)

    async def obter_por_codigo(self, codigo_consumo: str) -> ConsumoAgua:
        return await self._obter_ou_erro(codigo_consumo)

    async def listar(self, *, abastecimento_id: UUID | None=None, titular_id: UUID | None=None, referencia: str | None=None, status: StatusConsumo | None=None) -> list[ConsumoAgua]:
        return await self._consumo_repo.list(abastecimento_id=abastecimento_id, titular_id=titular_id, referencia=referencia, status=status)

    async def _obter_ou_erro(self, codigo_consumo: str) -> ConsumoAgua:
        item = await self._consumo_repo.get_by_codigo(codigo_consumo)
        if not item:
            raise ConsumoNotFoundError('Consumo nao encontrado')
        return item