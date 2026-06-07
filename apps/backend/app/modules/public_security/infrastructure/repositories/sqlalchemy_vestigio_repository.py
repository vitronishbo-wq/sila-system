from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.public_security.application.ports.vestigio_repository_port import (
    VestigioRepositoryPort,
)
from apps.backend.app.modules.public_security.domain.enums import StatusVestigio, TipoVestigio
from apps.backend.app.modules.public_security.domain.models.vestigio import Vestigio
from apps.backend.app.modules.public_security.infrastructure.models.vestigio_model import (
    VestigioModel,
)


class SQLAlchemyVestigioRepository(VestigioRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, vestigio: Vestigio) -> Vestigio:
        model = await self.session.get(VestigioModel, vestigio.id)
        if not model:
            model = VestigioModel(id=vestigio.id)
            self.session.add(model)
        model.codigo_vestigio = vestigio.codigo_vestigio
        model.cadeia_custodia_id = vestigio.cadeia_custodia_id
        model.ocorrencia_id = vestigio.ocorrencia_id
        model.tipo = vestigio.tipo.value
        model.descricao = vestigio.descricao
        model.localizacao = vestigio.localizacao
        model.data_coleta = vestigio.data_coleta
        model.status = vestigio.status.value
        model.coletado_por_id = vestigio.coletado_por_id
        model.observacoes = vestigio.observacoes
        model.ativo = vestigio.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, vestigio_id: UUID) -> Vestigio | None:
        model = await self.session.get(VestigioModel, vestigio_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_vestigio: str) -> Vestigio | None:
        stmt = select(VestigioModel).where(VestigioModel.codigo_vestigio == codigo_vestigio.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Vestigio]:
        stmt = select(VestigioModel).order_by(VestigioModel.data_coleta.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_cadeia(self, cadeia_custodia_id: UUID) -> list[Vestigio]:
        stmt = (
            select(VestigioModel)
            .where(VestigioModel.cadeia_custodia_id == cadeia_custodia_id)
            .order_by(VestigioModel.data_coleta.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusVestigio) -> list[Vestigio]:
        stmt = (
            select(VestigioModel)
            .where(VestigioModel.status == status.value)
            .order_by(VestigioModel.data_coleta.desc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, vestigio_id: UUID) -> bool:
        model = await self.session.get(VestigioModel, vestigio_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"VST/{year}/"
        stmt = (
            select(func.count())
            .select_from(VestigioModel)
            .where(VestigioModel.codigo_vestigio.like(f"{prefix}%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"{prefix}{count + 1:06d}"

    @staticmethod
    def _to_domain(model: VestigioModel) -> Vestigio:
        return Vestigio(
            id=model.id,
            codigo_vestigio=model.codigo_vestigio,
            cadeia_custodia_id=model.cadeia_custodia_id,
            ocorrencia_id=model.ocorrencia_id,
            tipo=TipoVestigio(model.tipo),
            descricao=model.descricao,
            localizacao=model.localizacao,
            data_coleta=model.data_coleta,
            status=StatusVestigio(model.status),
            coletado_por_id=model.coletado_por_id,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
