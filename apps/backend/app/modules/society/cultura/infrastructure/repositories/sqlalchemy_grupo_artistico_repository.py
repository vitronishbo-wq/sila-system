from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.cultura.application.ports.grupo_artistico_repository_port import GrupoArtisticoRepositoryPort
from apps.backend.app.modules.society.cultura.domain.enums import TipoGrupoArtistico
from apps.backend.app.modules.society.cultura.domain.models.grupo_artistico import GrupoArtistico
from apps.backend.app.modules.society.cultura.infrastructure.models.grupo_artistico_model import GrupoArtisticoModel

class SQLAlchemyGrupoArtisticoRepository(GrupoArtisticoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, grupo: GrupoArtistico) -> GrupoArtistico:
        model = await self.session.get(GrupoArtisticoModel, grupo.id)
        if not model:
            model = GrupoArtisticoModel(id=grupo.id)
            self.session.add(model)
        model.codigo_grupo = grupo.codigo_grupo
        model.nome = grupo.nome
        model.tipo = grupo.tipo.value
        model.lider_artista_id = grupo.lider_artista_id
        model.descricao = grupo.descricao
        model.data_fundacao = grupo.data_fundacao
        model.municipio = grupo.municipio
        model.provincia = grupo.provincia
        model.instituicao_educacional_id = grupo.instituicao_educacional_id
        model.membros_ids = [str(item) for item in grupo.membros_ids] if grupo.membros_ids else None
        model.data_cadastro = grupo.data_cadastro
        model.ativo = grupo.ativo
        model.observacoes = grupo.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, grupo_id: UUID) -> GrupoArtistico | None:
        model = await self.session.get(GrupoArtisticoModel, grupo_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_grupo: str) -> GrupoArtistico | None:
        stmt = select(GrupoArtisticoModel).where(GrupoArtisticoModel.codigo_grupo == codigo_grupo.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[GrupoArtistico]:
        stmt = select(GrupoArtisticoModel).order_by(GrupoArtisticoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoGrupoArtistico) -> list[GrupoArtistico]:
        stmt = select(GrupoArtisticoModel).where(GrupoArtisticoModel.tipo == tipo.value).order_by(GrupoArtisticoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[GrupoArtistico]:
        stmt = select(GrupoArtisticoModel).where(func.lower(GrupoArtisticoModel.municipio) == municipio.strip().lower()).order_by(GrupoArtisticoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, grupo_id: UUID) -> bool:
        model = await self.session.get(GrupoArtisticoModel, grupo_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(GrupoArtisticoModel).where(GrupoArtisticoModel.codigo_grupo.like(f'GRP/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'GRP/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: GrupoArtisticoModel) -> GrupoArtistico:
        return GrupoArtistico(id=model.id, codigo_grupo=model.codigo_grupo, nome=model.nome, tipo=TipoGrupoArtistico(model.tipo), lider_artista_id=model.lider_artista_id, data_cadastro=model.data_cadastro, descricao=model.descricao, data_fundacao=model.data_fundacao, municipio=model.municipio, provincia=model.provincia, instituicao_educacional_id=model.instituicao_educacional_id, membros_ids=[UUID(item) for item in model.membros_ids] if model.membros_ids else None, ativo=model.ativo, observacoes=model.observacoes)