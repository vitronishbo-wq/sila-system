from __future__ import annotations
from datetime import date
from app.modules.resources.agricultura.application.services.producao_service import ProducaoService
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.domain.models.safra import Safra
from app.modules.resources.agricultura.exceptions import SafraNotFoundError

class SafraService:

    def __init__(self, *, propriedade_service: PropriedadeService, producao_service: ProducaoService) -> None:
        self._propriedade_service = propriedade_service
        self._producao_service = producao_service
        self._items: dict[str, Safra] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f'SAF/{date.today().year}/{self._seq:06d}'

    async def criar_safra(self, *, codigo_propriedade: str, codigo_cultura: str, ano: int, area_plantada_ha: float, producao_estimada_ton: float) -> Safra:
        propriedade = await self._propriedade_service.obter(codigo_propriedade)
        cultura = await self._producao_service.obter_cultura(codigo_cultura)
        item = Safra.criar(propriedade_id=propriedade.id, cultura_id=cultura.id, ano=ano, area_plantada_ha=area_plantada_ha, producao_estimada_ton=producao_estimada_ton)
        item.codigo_safra = self._next_codigo()
        self._items[item.codigo_safra] = item
        return item

    async def iniciar(self, codigo_safra: str) -> Safra:
        item = self._items.get(codigo_safra)
        if not item:
            raise SafraNotFoundError('Safra nao encontrada')
        item.iniciar()
        return item

    async def colher(self, codigo_safra: str, producao_real_ton: float) -> Safra:
        item = self._items.get(codigo_safra)
        if not item:
            raise SafraNotFoundError('Safra nao encontrada')
        item.colher(producao_real_ton)
        return item

    async def obter(self, codigo_safra: str) -> Safra:
        item = self._items.get(codigo_safra)
        if not item:
            raise SafraNotFoundError('Safra nao encontrada')
        return item

    async def listar(self) -> list[Safra]:
        return list(self._items.values())