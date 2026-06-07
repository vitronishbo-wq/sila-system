from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.application.services.safra_service import (
    SafraService,
)
from apps.backend.app.modules.resources.agricultura.application.services.talhao_service import (
    TalhaoService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusPlantio, StatusSafra
from apps.backend.app.modules.resources.agricultura.domain.models.plantio import Plantio
from apps.backend.app.modules.resources.agricultura.exceptions import PlantioNotFoundError


class PlantioService:
    def __init__(self, *, safra_service: SafraService, talhao_service: TalhaoService) -> None:
        self._safra_service = safra_service
        self._talhao_service = talhao_service
        self._items: dict[str, Plantio] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f"PLA/{date.today().year}/{self._seq:06d}"

    async def planejar(
        self,
        *,
        codigo_safra: str,
        codigo_talhao: str,
        area_plantada_ha: float,
        quantidade_semente: float | None = None,
    ) -> Plantio:
        safra = await self._safra_service.obter(codigo_safra)
        talhao = await self._talhao_service.obter(codigo_talhao)
        if safra.status not in {StatusSafra.PLANEJADA, StatusSafra.EM_ANDAMENTO}:
            raise ValueError("Safra sem status valido para planejamento de plantio")
        if area_plantada_ha > talhao.area_ha:
            raise ValueError("Area plantada nao pode exceder area do talhao")
        item = Plantio.planejar(
            codigo_safra=codigo_safra,
            codigo_talhao=codigo_talhao,
            area_plantada_ha=area_plantada_ha,
            quantidade_semente=quantidade_semente,
        )
        item.codigo_plantio = self._next_codigo()
        self._items[item.codigo_plantio] = item
        return item

    async def executar(self, codigo_plantio: str) -> Plantio:
        item = self._items.get(codigo_plantio)
        if not item:
            raise PlantioNotFoundError("Plantio nao encontrado")
        item.executar()
        return item

    async def cancelar(self, codigo_plantio: str, *, motivo: str) -> Plantio:
        item = self._items.get(codigo_plantio)
        if not item:
            raise PlantioNotFoundError("Plantio nao encontrado")
        item.cancelar(motivo)
        return item

    async def obter(self, codigo_plantio: str) -> Plantio:
        item = self._items.get(codigo_plantio)
        if not item:
            raise PlantioNotFoundError("Plantio nao encontrado")
        return item

    async def listar(
        self,
        *,
        codigo_safra: str | None = None,
        codigo_talhao: str | None = None,
        status: StatusPlantio | None = None,
    ) -> list[Plantio]:
        values = list(self._items.values())
        if codigo_safra:
            values = [item for item in values if item.codigo_safra == codigo_safra]
        if codigo_talhao:
            values = [item for item in values if item.codigo_talhao == codigo_talhao]
        if status:
            values = [item for item in values if item.status == status]
        return values
