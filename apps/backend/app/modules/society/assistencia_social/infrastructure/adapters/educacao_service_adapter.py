from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from apps.backend.app.core.enums import StatusMatricula
from apps.backend.app.modules.society.assistencia_social.application.ports import (
    EducacaoServicePort,
)


class _MatriculaSnapshot(Protocol):
    status: StatusMatricula | str


class _MatriculaRepository(Protocol):
    async def get_by_citizen(
        self, citizen_id: UUID, ano_letivo_id: UUID | None = None
    ) -> Sequence[_MatriculaSnapshot]: ...


class EducacaoServiceAdapter(EducacaoServicePort):
    def __init__(self, matricula_repo: _MatriculaRepository):
        self._matricula_repo = matricula_repo

    async def is_estudante_ativo(self, citizen_id: UUID) -> bool:
        matriculas = await self._matricula_repo.get_by_citizen(citizen_id)
        return any(
            m.status
            in {
                StatusMatricula.ATIVA,
                StatusMatricula.PENDENTE,
                StatusMatricula.ATIVA.value,
                StatusMatricula.PENDENTE.value,
            }
            for m in matriculas
        )
