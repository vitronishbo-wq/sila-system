from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.public_security.application.ports.evidencia_repository_port import (
    EvidenciaRepositoryPort,
)
from apps.backend.app.modules.public_security.domain.enums import StatusEvidencia, TipoEvidencia
from apps.backend.app.modules.public_security.domain.models.evidencia import Evidencia
from apps.backend.app.modules.public_security.infrastructure.models.evidencia_model import (
    EvidenciaModel,
)


class SQLAlchemyEvidenciaRepository(EvidenciaRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, evidencia: Evidencia) -> Evidencia:
        model = await self.session.get(EvidenciaModel, evidencia.id)
        if not model:
            model = EvidenciaModel(id=evidencia.id)
            self.session.add(model)
        model.codigo_evidencia = evidencia.codigo_evidencia
        model.vestigio_id = evidencia.vestigio_id
        model.cadeia_custodia_id = evidencia.cadeia_custodia_id
        model.tipo = evidencia.tipo.value
        model.descricao = evidencia.descricao
        model.fonte = evidencia.fonte
        model.confiabilidade = evidencia.confiabilidade
        model.status = evidencia.status.value
        model.data_registro = evidencia.data_registro
        model.analisado_por_id = evidencia.analisado_por_id
        model.observacoes = evidencia.observacoes
        model.ativo = evidencia.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, evidencia_id: UUID) -> Evidencia | None:
        model = await self.session.get(EvidenciaModel, evidencia_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_evidencia: str) -> Evidencia | None:
        stmt = select(EvidenciaModel).where(
            EvidenciaModel.codigo_evidencia == codigo_evidencia.strip()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Evidencia]:
        stmt = select(EvidenciaModel).order_by(EvidenciaModel.data_registro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_vestigio(self, vestigio_id: UUID) -> list[Evidencia]:
        stmt = (
            select(EvidenciaModel)
            .where(EvidenciaModel.vestigio_id == vestigio_id)
            .order_by(EvidenciaModel.data_registro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusEvidencia) -> list[Evidencia]:
        stmt = (
            select(EvidenciaModel)
            .where(EvidenciaModel.status == status.value)
            .order_by(EvidenciaModel.data_registro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, evidencia_id: UUID) -> bool:
        model = await self.session.get(EvidenciaModel, evidencia_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"EVD/{year}/"
        stmt = (
            select(func.count())
            .select_from(EvidenciaModel)
            .where(EvidenciaModel.codigo_evidencia.like(f"{prefix}%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"{prefix}{count + 1:06d}"

    @staticmethod
    def _to_domain(model: EvidenciaModel) -> Evidencia:
        return Evidencia(
            id=model.id,
            codigo_evidencia=model.codigo_evidencia,
            vestigio_id=model.vestigio_id,
            cadeia_custodia_id=model.cadeia_custodia_id,
            tipo=TipoEvidencia(model.tipo),
            descricao=model.descricao,
            fonte=model.fonte,
            confiabilidade=model.confiabilidade,
            status=StatusEvidencia(model.status),
            data_registro=model.data_registro,
            analisado_por_id=model.analisado_por_id,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
