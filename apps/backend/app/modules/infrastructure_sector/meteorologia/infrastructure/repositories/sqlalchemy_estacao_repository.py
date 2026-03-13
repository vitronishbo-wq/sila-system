from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.meteorologia.application.ports.estacao_repository_port import EstacaoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.enums import StationStatus
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.models import EstacaoMeteorologica
from apps.backend.app.modules.infrastructure_sector.meteorologia.infrastructure.models.estacao_model import EstacaoMeteorologicaModel

class SQLAlchemyEstacaoRepository(EstacaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, estacao: EstacaoMeteorologica) -> EstacaoMeteorologica:
        model = await self.session.get(EstacaoMeteorologicaModel, estacao.id)
        if model is None:
            model = EstacaoMeteorologicaModel(id=estacao.id)
            self.session.add(model)
        model.codigo = (estacao.codigo or '').strip().upper()
        model.nome = estacao.nome or ''
        model.latitude = estacao.latitude
        model.longitude = estacao.longitude
        model.altitude = estacao.altitude
        model.status = estacao.status.value
        model.municipio = estacao.municipio
        model.provincia = estacao.provincia
        model.metadata_json = estacao.metadata
        model.updated_at = estacao.updated_at
        model.deleted_at = None
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, estacao_id: UUID) -> EstacaoMeteorologica | None:
        stmt = select(EstacaoMeteorologicaModel).where(EstacaoMeteorologicaModel.id == estacao_id, EstacaoMeteorologicaModel.deleted_at.is_(None))
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo: str) -> EstacaoMeteorologica | None:
        stmt = select(EstacaoMeteorologicaModel).where(EstacaoMeteorologicaModel.codigo == codigo.strip().upper(), EstacaoMeteorologicaModel.deleted_at.is_(None))
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self, limit: int=100, offset: int=0) -> list[EstacaoMeteorologica]:
        stmt = select(EstacaoMeteorologicaModel).where(EstacaoMeteorologicaModel.deleted_at.is_(None)).order_by(EstacaoMeteorologicaModel.created_at.desc()).offset(offset).limit(limit)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_active(self, provincia: str | None=None) -> list[EstacaoMeteorologica]:
        stmt = select(EstacaoMeteorologicaModel).where(EstacaoMeteorologicaModel.deleted_at.is_(None), EstacaoMeteorologicaModel.status == StationStatus.ACTIVE.value)
        if provincia:
            stmt = stmt.where(EstacaoMeteorologicaModel.provincia == provincia)
        stmt = stmt.order_by(EstacaoMeteorologicaModel.codigo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_filtered(self, *, provincia: str | None=None, status: StationStatus | None=None, limit: int=100, offset: int=0) -> list[EstacaoMeteorologica]:
        stmt = select(EstacaoMeteorologicaModel).where(EstacaoMeteorologicaModel.deleted_at.is_(None))
        if provincia:
            stmt = stmt.where(EstacaoMeteorologicaModel.provincia == provincia)
        if status is not None:
            stmt = stmt.where(EstacaoMeteorologicaModel.status == status.value)
        stmt = stmt.order_by(EstacaoMeteorologicaModel.created_at.desc()).offset(offset).limit(limit)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def delete(self, estacao_id: UUID) -> bool:
        model = await self.session.get(EstacaoMeteorologicaModel, estacao_id)
        if model is None or model.deleted_at is not None:
            return False
        model.deleted_at = datetime.now(timezone.utc)
        model.status = StationStatus.INACTIVE.value
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: EstacaoMeteorologicaModel) -> EstacaoMeteorologica:
        return EstacaoMeteorologica(estacao_id=model.id, codigo=model.codigo, nome=model.nome, latitude=model.latitude, longitude=model.longitude, altitude=model.altitude, status=StationStatus(model.status), municipio=model.municipio, provincia=model.provincia, metadata=model.metadata_json, created_at=model.created_at, updated_at=model.updated_at)