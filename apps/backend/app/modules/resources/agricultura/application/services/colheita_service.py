from __future__ import annotations
from datetime import date
from app.modules.resources.agricultura.application.services.safra_service import SafraService
from app.modules.resources.agricultura.application.services.talhao_service import TalhaoService
from app.modules.resources.agricultura.domain.enums import StatusSafra
from app.modules.resources.agricultura.domain.models.colheita import Colheita
from app.modules.resources.agricultura.exceptions import ColheitaNotFoundError

class ColheitaService:

    def __init__(self, *, safra_service: SafraService, talhao_service: TalhaoService) -> None:
        self._safra_service = safra_service
        self._talhao_service = talhao_service
        self._items: dict[str, Colheita] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f'COL/{date.today().year}/{self._seq:06d}'

    async def registrar(self, *, codigo_safra: str, codigo_talhao: str, quantidade_colhida_ton: float, perdas_ton: float=0.0, umidade_percentual: float | None=None, observacoes: str | None=None) -> Colheita:
        safra = await self._safra_service.obter(codigo_safra)
        await self._talhao_service.obter(codigo_talhao)
        if safra.status != StatusSafra.EM_ANDAMENTO:
            raise ValueError('Somente safra em andamento pode receber registro de colheita')
        item = Colheita.registrar(codigo_safra=codigo_safra, codigo_talhao=codigo_talhao, quantidade_colhida_ton=quantidade_colhida_ton, perdas_ton=perdas_ton, umidade_percentual=umidade_percentual, observacoes=observacoes)
        item.codigo_colheita = self._next_codigo()
        self._items[item.codigo_colheita] = item
        return item

    async def obter(self, codigo_colheita: str) -> Colheita:
        item = self._items.get(codigo_colheita)
        if not item:
            raise ColheitaNotFoundError('Colheita nao encontrada')
        return item

    async def listar(self, *, codigo_safra: str | None=None, codigo_talhao: str | None=None) -> list[Colheita]:
        values = list(self._items.values())
        if codigo_safra:
            values = [item for item in values if item.codigo_safra == codigo_safra]
        if codigo_talhao:
            values = [item for item in values if item.codigo_talhao == codigo_talhao]
        return values