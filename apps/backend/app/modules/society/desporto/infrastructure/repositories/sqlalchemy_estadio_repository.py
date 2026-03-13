from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.desporto.application.ports.estadio_repository_port import EstadioRepositoryPort
from apps.backend.app.modules.society.desporto.domain.enums import EstadoRelvado, TipoEstadio
from apps.backend.app.modules.society.desporto.domain.models.estadio import Estadio
from apps.backend.app.modules.society.desporto.infrastructure.models.estadio_model import EstadioModel

class SQLAlchemyEstadioRepository(EstadioRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, estadio: Estadio) -> Estadio:
        model = await self.session.get(EstadioModel, estadio.id)
        if not model:
            model = EstadioModel(id=estadio.id)
            self.session.add(model)
        model.codigo_estadio = estadio.codigo_estadio
        model.nome = estadio.nome
        model.tipo = estadio.tipo.value
        model.municipio = estadio.municipio
        model.provincia = estadio.provincia
        model.capacidade = estadio.capacidade
        model.estado_relvado = estadio.estado_relvado.value
        model.data_cadastro = estadio.data_cadastro
        model.codigo_obra_instalacao = estadio.codigo_obra_instalacao
        model.clube_mandante_id = estadio.clube_mandante_id
        model.ativo = estadio.ativo
        model.observacoes = estadio.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, estadio_id: UUID) -> Estadio | None:
        model = await self.session.get(EstadioModel, estadio_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_estadio: str) -> Estadio | None:
        stmt = select(EstadioModel).where(EstadioModel.codigo_estadio == codigo_estadio.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Estadio]:
        stmt = select(EstadioModel).order_by(EstadioModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[Estadio]:
        stmt = select(EstadioModel).where(func.lower(EstadioModel.municipio) == municipio.strip().lower()).order_by(EstadioModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, estadio_id: UUID) -> bool:
        model = await self.session.get(EstadioModel, estadio_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        stmt = select(func.count()).select_from(EstadioModel).where(EstadioModel.codigo_estadio.like(f'EST/{year}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'EST/{year}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: EstadioModel) -> Estadio:
        return Estadio(id=model.id, codigo_estadio=model.codigo_estadio, nome=model.nome, tipo=TipoEstadio(model.tipo), municipio=model.municipio, provincia=model.provincia, capacidade=model.capacidade, estado_relvado=EstadoRelvado(model.estado_relvado), data_cadastro=model.data_cadastro, codigo_obra_instalacao=model.codigo_obra_instalacao, clube_mandante_id=model.clube_mandante_id, ativo=model.ativo, observacoes=model.observacoes)