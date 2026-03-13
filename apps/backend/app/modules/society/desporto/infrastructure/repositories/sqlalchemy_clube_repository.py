from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.desporto.application.ports.clube_repository_port import ClubeRepositoryPort
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, TipoClube
from app.modules.society.desporto.domain.models.clube import Clube
from app.modules.society.desporto.infrastructure.models.clube_model import ClubeModel

class SQLAlchemyClubeRepository(ClubeRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, clube: Clube) -> Clube:
        model = await self.session.get(ClubeModel, clube.id)
        if not model:
            model = ClubeModel(id=clube.id)
            self.session.add(model)
        model.codigo_clube = clube.codigo_clube
        model.nome = clube.nome
        model.sigla = clube.sigla
        model.tipo = clube.tipo.value
        model.modalidade_principal = clube.modalidade_principal.value
        model.municipio = clube.municipio
        model.provincia = clube.provincia
        model.data_cadastro = clube.data_cadastro
        model.data_fundacao = clube.data_fundacao
        model.codigo_obra_instalacao = clube.codigo_obra_instalacao
        model.instituicao_educacional_id = clube.instituicao_educacional_id
        model.ativo = clube.ativo
        model.observacoes = clube.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, clube_id: UUID) -> Clube | None:
        model = await self.session.get(ClubeModel, clube_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_clube: str) -> Clube | None:
        stmt = select(ClubeModel).where(ClubeModel.codigo_clube == codigo_clube.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Clube]:
        stmt = select(ClubeModel).order_by(ClubeModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoClube) -> list[Clube]:
        stmt = select(ClubeModel).where(ClubeModel.tipo == tipo.value).order_by(ClubeModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Clube]:
        stmt = select(ClubeModel).where(ClubeModel.modalidade_principal == modalidade.value).order_by(ClubeModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[Clube]:
        stmt = select(ClubeModel).where(func.lower(ClubeModel.municipio) == municipio.strip().lower()).order_by(ClubeModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, clube_id: UUID) -> bool:
        model = await self.session.get(ClubeModel, clube_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(ClubeModel).where(ClubeModel.codigo_clube.like(f'CLB/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'CLB/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: ClubeModel) -> Clube:
        return Clube(id=model.id, codigo_clube=model.codigo_clube, nome=model.nome, sigla=model.sigla, tipo=TipoClube(model.tipo), modalidade_principal=ModalidadeDesportiva(model.modalidade_principal), municipio=model.municipio, provincia=model.provincia, data_cadastro=model.data_cadastro, data_fundacao=model.data_fundacao, codigo_obra_instalacao=model.codigo_obra_instalacao, instituicao_educacional_id=model.instituicao_educacional_id, ativo=model.ativo, observacoes=model.observacoes)