from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.domain.models.cultura import Cultura
from apps.backend.app.modules.resources.agricultura.exceptions import CulturaNotFoundError


class ProducaoService:
    def __init__(self) -> None:
        self._culturas: dict[str, Cultura] = {}
        self._seq_cultura = 0

    def _next_codigo_cultura(self) -> str:
        self._seq_cultura += 1
        return f"CULT/{date.today().year}/{self._seq_cultura:06d}"

    async def cadastrar_cultura(
        self, *, nome: str, tipo, ciclo_dias: int, produtividade_estimada_ton_ha: float
    ) -> Cultura:
        item = Cultura.criar(
            nome=nome,
            tipo=tipo,
            ciclo_dias=ciclo_dias,
            produtividade_estimada_ton_ha=produtividade_estimada_ton_ha,
        )
        item.codigo_cultura = self._next_codigo_cultura()
        self._culturas[item.codigo_cultura] = item
        return item

    async def obter_cultura(self, codigo_cultura: str) -> Cultura:
        item = self._culturas.get(codigo_cultura)
        if not item:
            raise CulturaNotFoundError("Cultura nao encontrada")
        return item

    async def listar_culturas(self) -> list[Cultura]:
        return list(self._culturas.values())
