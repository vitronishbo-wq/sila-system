from __future__ import annotations
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.educacao.application.ports import TurmaRepositoryPort
from apps.backend.app.modules.educacao.domain.models import Turma, Turno
from apps.backend.app.modules.educacao.domain.models.matricula import StatusMatricula
from apps.backend.app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel
from apps.backend.app.modules.educacao.infrastructure.models.turma_model import TurmaModel

class SQLAlchemyTurmaRepository(TurmaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: UUID) -> Turma | None:
        model = await self.session.get(TurmaModel, id)
        return self._to_domain(model) if model else None

    async def count_matriculas_ativas(self, turma_id: UUID, ano_letivo_id: UUID) -> int:
        stmt = select(func.count()).select_from(MatriculaModel).where(MatriculaModel.turma_id == turma_id, MatriculaModel.ano_letivo_id == ano_letivo_id, MatriculaModel.status.in_([StatusMatricula.PENDENTE.value, StatusMatricula.ATIVA.value]))
        return int((await self.session.execute(stmt)).scalar() or 0)

    @staticmethod
    def _to_domain(model: TurmaModel) -> Turma:
        return Turma(id=model.id, escola_id=model.escola_id, ano_letivo_id=model.ano_letivo_id, codigo=model.codigo, classe=model.classe, turno=Turno(model.turno), capacidade=model.capacidade, ativa=model.ativa)