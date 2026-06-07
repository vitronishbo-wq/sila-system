from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import (
    PropriedadeService,
)
from apps.backend.app.modules.resources.agricultura.domain.models.assistencia_tecnica import (
    AssistenciaTecnica,
)
from apps.backend.app.modules.resources.agricultura.exceptions import AssistenciaNotFoundError


class AssistenciaService:
    def __init__(self, *, propriedade_service: PropriedadeService) -> None:
        self._propriedade_service = propriedade_service
        self._items: dict[str, AssistenciaTecnica] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f"AST/{date.today().year}/{self._seq:06d}"

    async def agendar(
        self, *, codigo_propriedade: str, tecnico_nome: str, objetivo: str
    ) -> AssistenciaTecnica:
        await self._propriedade_service.obter(codigo_propriedade)
        item = AssistenciaTecnica.agendar(
            codigo_propriedade=codigo_propriedade, tecnico_nome=tecnico_nome, objetivo=objetivo
        )
        item.codigo_assistencia = self._next_codigo()
        self._items[item.codigo_assistencia] = item
        return item

    async def concluir(
        self, codigo_assistencia: str, *, recomendacoes: str | None = None
    ) -> AssistenciaTecnica:
        item = self._items.get(codigo_assistencia)
        if not item:
            raise AssistenciaNotFoundError("Assistencia tecnica nao encontrada")
        item.concluir(recomendacoes)
        return item

    async def cancelar(self, codigo_assistencia: str, *, motivo: str) -> AssistenciaTecnica:
        item = self._items.get(codigo_assistencia)
        if not item:
            raise AssistenciaNotFoundError("Assistencia tecnica nao encontrada")
        item.cancelar(motivo)
        return item

    async def obter(self, codigo_assistencia: str) -> AssistenciaTecnica:
        item = self._items.get(codigo_assistencia)
        if not item:
            raise AssistenciaNotFoundError("Assistencia tecnica nao encontrada")
        return item

    async def listar(self, *, codigo_propriedade: str | None = None) -> list[AssistenciaTecnica]:
        values = list(self._items.values())
        if codigo_propriedade:
            values = [item for item in values if item.codigo_propriedade == codigo_propriedade]
        return values
