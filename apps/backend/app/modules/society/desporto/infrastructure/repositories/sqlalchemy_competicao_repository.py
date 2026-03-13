from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.desporto.application.ports.competicao_repository_port import CompeticaoRepositoryPort
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusCompeticao, TipoCompeticao
from apps.backend.app.modules.society.desporto.domain.models.competicao import Competicao
from apps.backend.app.modules.society.desporto.infrastructure.models.competicao_model import CompeticaoModel

class SQLAlchemyCompeticaoRepository(CompeticaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, competicao: Competicao) -> Competicao:
        model = await self.session.get(CompeticaoModel, competicao.id)
        if not model:
            model = CompeticaoModel(id=competicao.id)
            self.session.add(model)
        model.codigo_competicao = competicao.codigo_competicao
        model.nome = competicao.nome
        model.tipo = competicao.tipo.value
        model.modalidade = competicao.modalidade.value
        model.data_inicio = competicao.data_inicio
        model.data_fim = competicao.data_fim
        model.municipio = competicao.municipio
        model.provincia = competicao.provincia
        model.organizador_id = competicao.organizador_id
        model.status = competicao.status.value
        model.codigo_obra_instalacao = competicao.codigo_obra_instalacao
        model.atracao_turistica_id = competicao.atracao_turistica_id
        model.instituicao_educacional_id = competicao.instituicao_educacional_id
        model.premiacao_total = competicao.premiacao_total
        model.inscricoes_abertas = competicao.inscricoes_abertas
        model.data_cadastro = competicao.data_cadastro
        model.ativo = competicao.ativo
        model.observacoes = competicao.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, competicao_id: UUID) -> Competicao | None:
        model = await self.session.get(CompeticaoModel, competicao_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_competicao: str) -> Competicao | None:
        stmt = select(CompeticaoModel).where(CompeticaoModel.codigo_competicao == codigo_competicao.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Competicao]:
        stmt = select(CompeticaoModel).order_by(CompeticaoModel.data_inicio.asc(), CompeticaoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoCompeticao) -> list[Competicao]:
        stmt = select(CompeticaoModel).where(CompeticaoModel.tipo == tipo.value).order_by(CompeticaoModel.data_inicio.asc(), CompeticaoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Competicao]:
        stmt = select(CompeticaoModel).where(CompeticaoModel.modalidade == modalidade.value).order_by(CompeticaoModel.data_inicio.asc(), CompeticaoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusCompeticao) -> list[Competicao]:
        stmt = select(CompeticaoModel).where(CompeticaoModel.status == status.value).order_by(CompeticaoModel.data_inicio.asc(), CompeticaoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[Competicao]:
        stmt = select(CompeticaoModel).where(CompeticaoModel.data_inicio >= data_inicio).where(CompeticaoModel.data_fim <= data_fim).order_by(CompeticaoModel.data_inicio.asc(), CompeticaoModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, competicao_id: UUID) -> bool:
        model = await self.session.get(CompeticaoModel, competicao_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(CompeticaoModel).where(CompeticaoModel.codigo_competicao.like(f'CMP/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'CMP/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: CompeticaoModel) -> Competicao:
        return Competicao(id=model.id, codigo_competicao=model.codigo_competicao, nome=model.nome, tipo=TipoCompeticao(model.tipo), modalidade=ModalidadeDesportiva(model.modalidade), data_inicio=model.data_inicio, data_fim=model.data_fim, municipio=model.municipio, provincia=model.provincia, organizador_id=model.organizador_id, data_cadastro=model.data_cadastro, status=StatusCompeticao(model.status), codigo_obra_instalacao=model.codigo_obra_instalacao, atracao_turistica_id=model.atracao_turistica_id, instituicao_educacional_id=model.instituicao_educacional_id, premiacao_total=model.premiacao_total, inscricoes_abertas=model.inscricoes_abertas, ativo=model.ativo, observacoes=model.observacoes)