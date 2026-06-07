from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import (
    PropriedadeService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusTalhao
from apps.backend.app.modules.resources.agricultura.domain.models.talhao import Talhao
from apps.backend.app.modules.resources.agricultura.exceptions import TalhaoNotFoundError


class TalhaoService:
    def __init__(self, *, propriedade_service: PropriedadeService) -> None:
        self._propriedade_service = propriedade_service
        self._items: dict[str, Talhao] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f"TAL/{date.today().year}/{self._seq:06d}"

    async def cadastrar(
        self,
        *,
        codigo_propriedade: str,
        nome: str,
        area_ha: float,
        tipo_solo: str | None = None,
        irrigado: bool = False,
    ) -> Talhao:
        await self._propriedade_service.obter(codigo_propriedade)
        item = Talhao.criar(
            codigo_propriedade=codigo_propriedade,
            nome=nome,
            area_ha=area_ha,
            tipo_solo=tipo_solo,
            irrigado=irrigado,
        )
        item.codigo_talhao = self._next_codigo()
        self._items[item.codigo_talhao] = item
        return item

    async def ativar(self, codigo_talhao: str) -> Talhao:
        item = self._items.get(codigo_talhao)
        if not item:
            raise TalhaoNotFoundError("Talhao nao encontrado")
        item.ativar()
        return item

    async def desativar(self, codigo_talhao: str) -> Talhao:
        item = self._items.get(codigo_talhao)
        if not item:
            raise TalhaoNotFoundError("Talhao nao encontrado")
        item.desativar()
        return item

    async def obter(self, codigo_talhao: str) -> Talhao:
        item = self._items.get(codigo_talhao)
        if not item:
            raise TalhaoNotFoundError("Talhao nao encontrado")
        return item

    async def listar(
        self, *, codigo_propriedade: str | None = None, status: StatusTalhao | None = None
    ) -> list[Talhao]:
        values = list(self._items.values())
        if codigo_propriedade:
            values = [item for item in values if item.codigo_propriedade == codigo_propriedade]
        if status:
            values = [item for item in values if item.status == status]
        return values
