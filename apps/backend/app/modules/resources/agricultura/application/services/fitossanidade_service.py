from __future__ import annotations

from datetime import date

from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import (
    PropriedadeService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusOcorrencia
from apps.backend.app.modules.resources.agricultura.domain.models.ocorrencia_fitossanitaria import (
    OcorrenciaFitossanitaria,
)
from apps.backend.app.modules.resources.agricultura.exceptions import OcorrenciaNotFoundError


class FitossanidadeService:
    def __init__(self, *, propriedade_service: PropriedadeService) -> None:
        self._propriedade_service = propriedade_service
        self._items: dict[str, OcorrenciaFitossanitaria] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f"FIT/{date.today().year}/{self._seq:06d}"

    async def registrar_ocorrencia(
        self,
        *,
        codigo_propriedade: str,
        praga_doenca: str,
        descricao: str,
        severidade,
        cultura_afetada: str | None = None,
        acao_recomendada: str | None = None,
    ) -> OcorrenciaFitossanitaria:
        await self._propriedade_service.obter(codigo_propriedade)
        item = OcorrenciaFitossanitaria.registrar(
            codigo_propriedade=codigo_propriedade,
            praga_doenca=praga_doenca,
            descricao=descricao,
            severidade=severidade,
            cultura_afetada=cultura_afetada,
            acao_recomendada=acao_recomendada,
        )
        item.codigo_ocorrencia = self._next_codigo()
        self._items[item.codigo_ocorrencia] = item
        return item

    async def iniciar_tratamento(self, codigo_ocorrencia: str) -> OcorrenciaFitossanitaria:
        item = self._items.get(codigo_ocorrencia)
        if not item:
            raise OcorrenciaNotFoundError("Ocorrencia fitossanitaria nao encontrada")
        item.iniciar_tratamento()
        return item

    async def resolver(self, codigo_ocorrencia: str) -> OcorrenciaFitossanitaria:
        item = self._items.get(codigo_ocorrencia)
        if not item:
            raise OcorrenciaNotFoundError("Ocorrencia fitossanitaria nao encontrada")
        item.resolver()
        return item

    async def obter(self, codigo_ocorrencia: str) -> OcorrenciaFitossanitaria:
        item = self._items.get(codigo_ocorrencia)
        if not item:
            raise OcorrenciaNotFoundError("Ocorrencia fitossanitaria nao encontrada")
        return item

    async def listar(
        self, *, codigo_propriedade: str | None = None, status: StatusOcorrencia | None = None
    ) -> list[OcorrenciaFitossanitaria]:
        values = list(self._items.values())
        if codigo_propriedade:
            values = [item for item in values if item.codigo_propriedade == codigo_propriedade]
        if status:
            values = [item for item in values if item.status == status]
        return values
