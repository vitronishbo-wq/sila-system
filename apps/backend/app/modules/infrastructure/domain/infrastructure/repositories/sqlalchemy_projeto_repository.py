from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure.application.ports.projeto_repository_port import ProjetoRepositoryPort
from apps.backend.app.modules.infrastructure.domain.enums import StatusProjeto, TipoProjeto
from apps.backend.app.modules.infrastructure.domain.models.projeto_obra import ProjetoObra
from apps.backend.app.modules.infrastructure.infrastructure.models.projeto_model import ProjetoModel

class SQLAlchemyProjetoRepository(ProjetoRepositoryPort):
    """Repository com ORM real (AsyncSession) e fallback em memoria."""

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, ProjetoObra] = {}
        self._seq = 0

    async def save(self, item: ProjetoObra) -> ProjetoObra:
        if self._session:
            existing = await self._session.execute(select(ProjetoModel).where(ProjetoModel.codigo_projeto == item.codigo_projeto))
            model = existing.scalars().first()
            if model is None:
                model = ProjetoModel(id=item.id, codigo_projeto=item.codigo_projeto, nome=item.nome, tipo=item.tipo.value, status=item.status.value, orgao_responsavel_id=item.orgao_responsavel_id, responsavel_tecnico_id=item.responsavel_tecnico_id, valor_estimado=item.valor_estimado, data_inicio_prevista=item.data_inicio_prevista, data_fim_prevista=item.data_fim_prevista, data_cadastro=item.data_cadastro, obra_id=item.obra_id, descricao=item.descricao, data_inicio_real=item.data_inicio_real, data_fim_real=item.data_fim_real, versao=item.versao, data_atualizacao=item.data_atualizacao, observacoes=item.observacoes)
                self._session.add(model)
            else:
                model.nome = item.nome
                model.tipo = item.tipo.value
                model.status = item.status.value
                model.orgao_responsavel_id = item.orgao_responsavel_id
                model.responsavel_tecnico_id = item.responsavel_tecnico_id
                model.valor_estimado = item.valor_estimado
                model.data_inicio_prevista = item.data_inicio_prevista
                model.data_fim_prevista = item.data_fim_prevista
                model.data_cadastro = item.data_cadastro
                model.obra_id = item.obra_id
                model.descricao = item.descricao
                model.data_inicio_real = item.data_inicio_real
                model.data_fim_real = item.data_fim_real
                model.versao = item.versao
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.codigo_projeto] = item
        return item

    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoObra | None:
        if self._session:
            result = await self._session.execute(select(ProjetoModel).where(ProjetoModel.codigo_projeto == codigo_projeto))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(codigo_projeto)

    async def list(self, *, status: StatusProjeto | None=None, tipo: TipoProjeto | None=None, orgao_responsavel_id: UUID | None=None, obra_id: UUID | None=None) -> list[ProjetoObra]:
        if self._session:
            statement = select(ProjetoModel)
            if status:
                statement = statement.where(ProjetoModel.status == status.value)
            if tipo:
                statement = statement.where(ProjetoModel.tipo == tipo.value)
            if orgao_responsavel_id:
                statement = statement.where(ProjetoModel.orgao_responsavel_id == orgao_responsavel_id)
            if obra_id:
                statement = statement.where(ProjetoModel.obra_id == obra_id)
            result = await self._session.execute(statement.order_by(ProjetoModel.codigo_projeto.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        if orgao_responsavel_id:
            values = [item for item in values if item.orgao_responsavel_id == orgao_responsavel_id]
        if obra_id:
            values = [item for item in values if item.obra_id == obra_id]
        return values

    async def next_codigo(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'PRJ/{year}/'
            result = await self._session.execute(select(func.count()).select_from(ProjetoModel).where(ProjetoModel.codigo_projeto.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'PRJ/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: ProjetoModel) -> ProjetoObra:
        return ProjetoObra(id=model.id, codigo_projeto=model.codigo_projeto, nome=model.nome, tipo=TipoProjeto(model.tipo), status=StatusProjeto(model.status), orgao_responsavel_id=model.orgao_responsavel_id, responsavel_tecnico_id=model.responsavel_tecnico_id, valor_estimado=Decimal(model.valor_estimado), data_inicio_prevista=model.data_inicio_prevista, data_fim_prevista=model.data_fim_prevista, data_cadastro=model.data_cadastro, obra_id=model.obra_id, descricao=model.descricao, data_inicio_real=model.data_inicio_real, data_fim_real=model.data_fim_real, versao=model.versao, data_atualizacao=model.data_atualizacao, observacoes=model.observacoes)
