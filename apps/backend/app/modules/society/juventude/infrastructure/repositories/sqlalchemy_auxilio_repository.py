from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.juventude.application.ports.auxilio_repository_port import (
    AuxilioRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusBeneficio, TipoAuxilio
from apps.backend.app.modules.society.juventude.domain.models.auxilio import Auxilio
from apps.backend.app.modules.society.juventude.infrastructure.models.auxilio_model import (
    AuxilioModel,
)


class SQLAlchemyAuxilioRepository(AuxilioRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, auxilio: Auxilio) -> Auxilio:
        model = await self.session.get(AuxilioModel, auxilio.id)
        if not model:
            model = AuxilioModel(id=auxilio.id)
            self.session.add(model)
        model.codigo_auxilio = auxilio.codigo_auxilio
        model.jovem_id = auxilio.jovem_id
        model.tipo = auxilio.tipo.value
        model.data_inicio = auxilio.data_inicio
        model.data_fim = auxilio.data_fim
        model.valor_mensal = auxilio.valor_mensal
        model.status = auxilio.status.value
        model.data_cadastro = auxilio.data_cadastro
        model.observacoes = auxilio.observacoes
        model.ativo = auxilio.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, auxilio_id: UUID) -> Auxilio | None:
        model = await self.session.get(AuxilioModel, auxilio_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_auxilio: str) -> Auxilio | None:
        stmt = select(AuxilioModel).where(AuxilioModel.codigo_auxilio == codigo_auxilio.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Auxilio]:
        stmt = select(AuxilioModel).order_by(AuxilioModel.data_cadastro.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_jovem(self, jovem_id: UUID) -> list[Auxilio]:
        stmt = (
            select(AuxilioModel)
            .where(AuxilioModel.jovem_id == jovem_id)
            .order_by(AuxilioModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoAuxilio) -> list[Auxilio]:
        stmt = (
            select(AuxilioModel)
            .where(AuxilioModel.tipo == tipo.value)
            .order_by(AuxilioModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusBeneficio) -> list[Auxilio]:
        stmt = (
            select(AuxilioModel)
            .where(AuxilioModel.status == status.value)
            .order_by(AuxilioModel.data_cadastro.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, auxilio_id: UUID) -> bool:
        model = await self.session.get(AuxilioModel, auxilio_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(AuxilioModel)
            .where(AuxilioModel.codigo_auxilio.like(f"AUX/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"AUX/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: AuxilioModel) -> Auxilio:
        return Auxilio(
            id=model.id,
            codigo_auxilio=model.codigo_auxilio,
            jovem_id=model.jovem_id,
            tipo=TipoAuxilio(model.tipo),
            data_inicio=model.data_inicio,
            data_fim=model.data_fim,
            valor_mensal=model.valor_mensal,
            status=StatusBeneficio(model.status),
            data_cadastro=model.data_cadastro,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
