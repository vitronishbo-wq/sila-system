from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.ports import MatriculaRepositoryPort
from apps.backend.app.modules.educacao.domain.models import Matricula, StatusMatricula
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel


class SQLAlchemyMatriculaRepository(MatriculaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, matricula: Matricula) -> Matricula:
        model = await self.session.get(MatriculaModel, matricula.id)
        if not model:
            model = MatriculaModel(id=matricula.id)
            self.session.add(model)
        model.numero_processo = matricula.numero_processo
        model.citizen_id = matricula.citizen_id
        model.escola_id = matricula.escola_id
        model.turma_id = matricula.turma_id
        model.ano_letivo_id = matricula.ano_letivo_id
        model.data_matricula = matricula.data_matricula
        model.status = matricula.status.value
        model.observacoes = matricula.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID):
        model = await self.session.get(MatriculaModel, id)
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID, ano_letivo_id: UUID | None = None):
        stmt = select(MatriculaModel).where(MatriculaModel.citizen_id == citizen_id)
        if ano_letivo_id:
            stmt = stmt.where(MatriculaModel.ano_letivo_id == ano_letivo_id)
        stmt = stmt.order_by(MatriculaModel.data_matricula.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def get_by_escola(self, escola_id: UUID, ano_letivo_id: UUID):
        stmt = select(MatriculaModel).where(
            MatriculaModel.escola_id == escola_id, MatriculaModel.ano_letivo_id == ano_letivo_id
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def exists_active_for_citizen(self, citizen_id: UUID, ano_letivo_id: UUID) -> bool:
        stmt = select(MatriculaModel.id).where(
            and_(
                MatriculaModel.citizen_id == citizen_id,
                MatriculaModel.ano_letivo_id == ano_letivo_id,
                MatriculaModel.status.in_(
                    [StatusMatricula.PENDENTE.value, StatusMatricula.ATIVA.value]
                ),
            )
        )
        return (await self.session.execute(stmt)).first() is not None

    async def next_numero_processo(self, ano: int, escola_id: UUID) -> str:
        escola_stmt = select(EscolaModel).where(EscolaModel.id == escola_id)
        escola = (await self.session.execute(escola_stmt)).scalars().first()
        if escola and escola.codigo_med:
            codigo = "".join(ch for ch in escola.codigo_med if ch.isalnum())[-5:].upper()
        else:
            codigo = "00000"
        prefix = f"{ano}/{codigo}/"
        count_stmt = (
            select(func.count())
            .select_from(MatriculaModel)
            .where(MatriculaModel.numero_processo.like(f"{prefix}%"))
        )
        count = (await self.session.execute(count_stmt)).scalar() or 0
        return f"{prefix}{count + 1:04d}"

    @staticmethod
    def _to_domain(model: MatriculaModel) -> Matricula:
        # Be tolerant of legacy/variant status strings stored in the DB.
        try:
            status = StatusMatricula(model.status)
        except Exception:
            # Known legacy mapping: 'confirmada' (legacy) -> 'concluida' (current)
            legacy_map = {"confirmada": "concluida", "confirmado": "concluida"}
            mapped = legacy_map.get(str(model.status).lower())
            try:
                status = StatusMatricula(mapped) if mapped else StatusMatricula.PENDENTE
            except Exception:
                status = StatusMatricula.PENDENTE

        return Matricula(
            id=model.id,
            numero_processo=model.numero_processo,
            citizen_id=model.citizen_id,
            escola_id=model.escola_id,
            turma_id=model.turma_id,
            ano_letivo_id=model.ano_letivo_id,
            data_matricula=model.data_matricula or date.today(),
            status=status,
            observacoes=model.observacoes,
        )
