from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.cultura.application.ports.evento_cultural_repository_port import EventoCulturalRepositoryPort
from apps.backend.app.modules.society.cultura.domain.enums import StatusEventoCultural, TipoEventoCultural
from apps.backend.app.modules.society.cultura.domain.models.evento_cultural import EventoCultural
from apps.backend.app.modules.society.cultura.infrastructure.models.evento_cultural_model import EventoCulturalModel

class SQLAlchemyEventoCulturalRepository(EventoCulturalRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, evento: EventoCultural) -> EventoCultural:
        model = await self.session.get(EventoCulturalModel, evento.id)
        if not model:
            model = EventoCulturalModel(id=evento.id)
            self.session.add(model)
        model.codigo_evento = evento.codigo_evento
        model.nome = evento.nome
        model.tipo = evento.tipo.value
        model.descricao = evento.descricao
        model.data_inicio = evento.data_inicio
        model.data_fim = evento.data_fim
        model.local = evento.local
        model.municipio = evento.municipio
        model.provincia = evento.provincia
        model.realizador_id = evento.realizador_id
        model.atracao_turistica_id = evento.atracao_turistica_id
        model.instituicao_educacional_id = evento.instituicao_educacional_id
        model.entrada_gratuita = evento.entrada_gratuita
        model.valor_ingresso = evento.valor_ingresso
        model.publico_estimado = evento.publico_estimado
        model.status = evento.status.value
        model.data_cadastro = evento.data_cadastro
        model.ativo = evento.ativo
        model.observacoes = evento.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, evento_id: UUID) -> EventoCultural | None:
        model = await self.session.get(EventoCulturalModel, evento_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_evento: str) -> EventoCultural | None:
        stmt = select(EventoCulturalModel).where(EventoCulturalModel.codigo_evento == codigo_evento.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[EventoCultural]:
        stmt = select(EventoCulturalModel).order_by(EventoCulturalModel.data_inicio.asc(), EventoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoEventoCultural) -> list[EventoCultural]:
        stmt = select(EventoCulturalModel).where(EventoCulturalModel.tipo == tipo.value).order_by(EventoCulturalModel.data_inicio.asc(), EventoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[EventoCultural]:
        stmt = select(EventoCulturalModel).where(func.lower(EventoCulturalModel.municipio) == municipio.strip().lower()).order_by(EventoCulturalModel.data_inicio.asc(), EventoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusEventoCultural) -> list[EventoCultural]:
        stmt = select(EventoCulturalModel).where(EventoCulturalModel.status == status.value).order_by(EventoCulturalModel.data_inicio.asc(), EventoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[EventoCultural]:
        stmt = select(EventoCulturalModel).where(EventoCulturalModel.data_inicio >= data_inicio).where(EventoCulturalModel.data_fim <= data_fim).order_by(EventoCulturalModel.data_inicio.asc(), EventoCulturalModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, evento_id: UUID) -> bool:
        model = await self.session.get(EventoCulturalModel, evento_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(EventoCulturalModel).where(EventoCulturalModel.codigo_evento.like(f'EVT/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'EVT/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: EventoCulturalModel) -> EventoCultural:
        return EventoCultural(id=model.id, codigo_evento=model.codigo_evento, nome=model.nome, tipo=TipoEventoCultural(model.tipo), descricao=model.descricao, data_inicio=model.data_inicio, data_fim=model.data_fim, local=model.local, municipio=model.municipio, provincia=model.provincia, realizador_id=model.realizador_id, data_cadastro=model.data_cadastro, status=StatusEventoCultural(model.status), atracao_turistica_id=model.atracao_turistica_id, instituicao_educacional_id=model.instituicao_educacional_id, entrada_gratuita=model.entrada_gratuita, valor_ingresso=model.valor_ingresso, publico_estimado=model.publico_estimado, ativo=model.ativo, observacoes=model.observacoes)