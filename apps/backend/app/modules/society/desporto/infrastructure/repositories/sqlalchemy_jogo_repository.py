from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.desporto.application.ports.jogo_repository_port import JogoRepositoryPort
from app.modules.society.desporto.domain.enums import StatusJogo
from app.modules.society.desporto.domain.models.jogo import Jogo
from app.modules.society.desporto.infrastructure.models.jogo_model import JogoModel

class SQLAlchemyJogoRepository(JogoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, jogo: Jogo) -> Jogo:
        model = await self.session.get(JogoModel, jogo.id)
        if not model:
            model = JogoModel(id=jogo.id)
            self.session.add(model)
        model.codigo_jogo = jogo.codigo_jogo
        model.competicao_id = jogo.competicao_id
        model.clube_casa_id = jogo.clube_casa_id
        model.clube_fora_id = jogo.clube_fora_id
        model.data_jogo = jogo.data_jogo
        model.local = jogo.local
        model.municipio = jogo.municipio
        model.provincia = jogo.provincia
        model.data_cadastro = jogo.data_cadastro
        model.status = jogo.status.value
        model.placar_casa = jogo.placar_casa
        model.placar_fora = jogo.placar_fora
        model.codigo_obra_instalacao = jogo.codigo_obra_instalacao
        model.atracao_turistica_id = jogo.atracao_turistica_id
        model.publico_estimado = jogo.publico_estimado
        model.publico_presente = jogo.publico_presente
        model.ativo = jogo.ativo
        model.observacoes = jogo.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, jogo_id: UUID) -> Jogo | None:
        model = await self.session.get(JogoModel, jogo_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_jogo: str) -> Jogo | None:
        stmt = select(JogoModel).where(JogoModel.codigo_jogo == codigo_jogo.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Jogo]:
        stmt = select(JogoModel).order_by(JogoModel.data_jogo.asc(), JogoModel.codigo_jogo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_competicao(self, competicao_id: UUID) -> list[Jogo]:
        stmt = select(JogoModel).where(JogoModel.competicao_id == competicao_id).order_by(JogoModel.data_jogo.asc(), JogoModel.codigo_jogo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_clube(self, clube_id: UUID) -> list[Jogo]:
        stmt = select(JogoModel).where(or_(JogoModel.clube_casa_id == clube_id, JogoModel.clube_fora_id == clube_id)).order_by(JogoModel.data_jogo.asc(), JogoModel.codigo_jogo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusJogo) -> list[Jogo]:
        stmt = select(JogoModel).where(JogoModel.status == status.value).order_by(JogoModel.data_jogo.asc(), JogoModel.codigo_jogo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[Jogo]:
        stmt = select(JogoModel).where(JogoModel.data_jogo >= data_inicio).where(JogoModel.data_jogo <= data_fim).order_by(JogoModel.data_jogo.asc(), JogoModel.codigo_jogo.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, jogo_id: UUID) -> bool:
        model = await self.session.get(JogoModel, jogo_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(JogoModel).where(JogoModel.codigo_jogo.like(f'JOG/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'JOG/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: JogoModel) -> Jogo:
        return Jogo(id=model.id, codigo_jogo=model.codigo_jogo, competicao_id=model.competicao_id, clube_casa_id=model.clube_casa_id, clube_fora_id=model.clube_fora_id, data_jogo=model.data_jogo, local=model.local, municipio=model.municipio, provincia=model.provincia, data_cadastro=model.data_cadastro, status=StatusJogo(model.status), placar_casa=model.placar_casa, placar_fora=model.placar_fora, codigo_obra_instalacao=model.codigo_obra_instalacao, atracao_turistica_id=model.atracao_turistica_id, publico_estimado=model.publico_estimado, publico_presente=model.publico_presente, ativo=model.ativo, observacoes=model.observacoes)