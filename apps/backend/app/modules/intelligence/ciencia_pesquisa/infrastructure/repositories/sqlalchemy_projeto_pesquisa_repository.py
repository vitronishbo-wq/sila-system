from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.intelligence.ciencia_pesquisa.application.ports.projeto_pesquisa_repository_port import ProjetoPesquisaRepositoryPort
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.enums import AreaConhecimento, StatusProjetoPesquisa
from apps.backend.app.modules.intelligence.ciencia_pesquisa.domain.models.projeto_pesquisa import ProjetoPesquisa
from apps.backend.app.modules.intelligence.ciencia_pesquisa.infrastructure.models.projeto_pesquisa_model import ProjetoPesquisaModel

class SQLAlchemyProjetoPesquisaRepository(ProjetoPesquisaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, projeto: ProjetoPesquisa) -> ProjetoPesquisa:
        model = await self.session.get(ProjetoPesquisaModel, projeto.id)
        if not model:
            model = ProjetoPesquisaModel(id=projeto.id)
            self.session.add(model)
        model.codigo_projeto = projeto.codigo_projeto
        model.titulo = projeto.titulo
        model.resumo = projeto.resumo
        model.instituicao_id = projeto.instituicao_id
        model.coordenador_id = projeto.coordenador_id
        model.equipe_pesquisadores_ids = projeto.equipe_pesquisadores_ids
        model.area_conhecimento = projeto.area_conhecimento.value
        model.data_inicio = projeto.data_inicio
        model.data_fim_prevista = projeto.data_fim_prevista
        model.data_fim_real = projeto.data_fim_real
        model.status = projeto.status.value
        model.palavras_chave = projeto.palavras_chave
        model.orcamento_previsto = projeto.orcamento_previsto
        model.ativo = projeto.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, projeto_id: UUID) -> ProjetoPesquisa | None:
        model = await self.session.get(ProjetoPesquisaModel, projeto_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoPesquisa | None:
        stmt = select(ProjetoPesquisaModel).where(ProjetoPesquisaModel.codigo_projeto == codigo_projeto.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[ProjetoPesquisa]:
        stmt = select(ProjetoPesquisaModel).order_by(ProjetoPesquisaModel.codigo_projeto.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_instituicao(self, instituicao_id: UUID) -> list[ProjetoPesquisa]:
        stmt = select(ProjetoPesquisaModel).where(ProjetoPesquisaModel.instituicao_id == instituicao_id).order_by(ProjetoPesquisaModel.codigo_projeto.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_pesquisador(self, pesquisador_id: UUID) -> list[ProjetoPesquisa]:
        stmt = select(ProjetoPesquisaModel).where(ProjetoPesquisaModel.equipe_pesquisadores_ids.contains([pesquisador_id])).order_by(ProjetoPesquisaModel.codigo_projeto.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def vincular_pesquisadores(self, *, projeto_id: UUID, pesquisador_ids: list[UUID]) -> ProjetoPesquisa | None:
        model = await self.session.get(ProjetoPesquisaModel, projeto_id)
        if not model:
            return None
        equipe_atual = list(model.equipe_pesquisadores_ids or [])
        for pesquisador_id in pesquisador_ids:
            if pesquisador_id not in equipe_atual:
                equipe_atual.append(pesquisador_id)
        if model.coordenador_id not in equipe_atual:
            equipe_atual.append(model.coordenador_id)
        model.equipe_pesquisadores_ids = equipe_atual
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def delete(self, projeto_id: UUID) -> bool:
        model = await self.session.get(ProjetoPesquisaModel, projeto_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'PROJ/{year}/'
        stmt = select(func.count()).select_from(ProjetoPesquisaModel).where(ProjetoPesquisaModel.codigo_projeto.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:05d}'

    @staticmethod
    def _to_domain(model: ProjetoPesquisaModel) -> ProjetoPesquisa:
        orcamento = model.orcamento_previsto
        if isinstance(orcamento, Decimal):
            orcamento = float(orcamento)
        return ProjetoPesquisa(id=model.id, codigo_projeto=model.codigo_projeto, titulo=model.titulo, resumo=model.resumo, instituicao_id=model.instituicao_id, coordenador_id=model.coordenador_id, equipe_pesquisadores_ids=list(model.equipe_pesquisadores_ids or []), area_conhecimento=AreaConhecimento(model.area_conhecimento), data_inicio=model.data_inicio, data_fim_prevista=model.data_fim_prevista, data_fim_real=model.data_fim_real, status=StatusProjetoPesquisa(model.status), palavras_chave=list(model.palavras_chave or []), orcamento_previsto=orcamento, ativo=model.ativo)