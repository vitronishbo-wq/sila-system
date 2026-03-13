from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.juventude.application.ports.evento_juvenil_repository_port import EventoJuvenilRepositoryPort
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, StatusEvento, TipoEvento
from apps.backend.app.modules.society.juventude.domain.models.evento_juvenil import EventoJuvenil
from apps.backend.app.modules.society.juventude.infrastructure.models.evento_juvenil_model import EventoJuvenilModel

class SQLAlchemyEventoJuvenilRepository(EventoJuvenilRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, evento: EventoJuvenil) -> EventoJuvenil:
        model = await self.session.get(EventoJuvenilModel, evento.id)
        if not model:
            model = EventoJuvenilModel(id=evento.id)
            self.session.add(model)
        model.codigo_evento = evento.codigo_evento
        model.titulo = evento.titulo
        model.tipo_evento = evento.tipo_evento.value
        model.area_interesse = evento.area_interesse.value
        model.data_evento = evento.data_evento
        model.local = evento.local
        model.municipio = evento.municipio
        model.provincia = evento.provincia
        model.vagas = evento.vagas
        model.participantes = evento.participantes
        model.status = evento.status.value
        model.data_cadastro = evento.data_cadastro
        model.observacoes = evento.observacoes
        model.ativo = evento.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, evento_id: UUID) -> EventoJuvenil | None:
        model = await self.session.get(EventoJuvenilModel, evento_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_evento: str) -> EventoJuvenil | None:
        stmt = select(EventoJuvenilModel).where(EventoJuvenilModel.codigo_evento == codigo_evento.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[EventoJuvenil]:
        stmt = select(EventoJuvenilModel).order_by(EventoJuvenilModel.data_evento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def list_by_status(self, status: StatusEvento) -> list[EventoJuvenil]:
        stmt = select(EventoJuvenilModel).where(EventoJuvenilModel.status == status.value).order_by(EventoJuvenilModel.data_evento.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(i) for i in rows]

    async def delete(self, evento_id: UUID) -> bool:
        model = await self.session.get(EventoJuvenilModel, evento_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(EventoJuvenilModel).where(EventoJuvenilModel.codigo_evento.like(f'EVT/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'EVT/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: EventoJuvenilModel) -> EventoJuvenil:
        return EventoJuvenil(id=model.id, codigo_evento=model.codigo_evento, titulo=model.titulo, tipo_evento=TipoEvento(model.tipo_evento), area_interesse=AreaInteresse(model.area_interesse), data_evento=model.data_evento, local=model.local, municipio=model.municipio, provincia=model.provincia, vagas=model.vagas, participantes=model.participantes, status=StatusEvento(model.status), data_cadastro=model.data_cadastro or date.today(), observacoes=model.observacoes, ativo=model.ativo)