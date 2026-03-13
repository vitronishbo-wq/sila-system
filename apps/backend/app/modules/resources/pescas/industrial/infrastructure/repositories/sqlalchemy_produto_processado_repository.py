from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pescas.industrial.application.ports.produto_processado_repository_port import ProdutoProcessadoRepositoryPort
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import MercadoDestino, TipoProcessamento, TipoProdutoProcessado
from apps.backend.app.modules.resources.pescas.industrial.domain.models.produto_processado import ProdutoProcessado
from apps.backend.app.modules.resources.pescas.industrial.infrastructure.models.produto_processado_model import ProdutoProcessadoModel

class SQLAlchemyProdutoProcessadoRepository(ProdutoProcessadoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, produto: ProdutoProcessado) -> ProdutoProcessado:
        model = await self.session.get(ProdutoProcessadoModel, produto.id)
        if not model:
            model = ProdutoProcessadoModel(id=produto.id)
            self.session.add(model)
        model.codigo_produto = produto.codigo_produto
        model.unidade_processamento_id = produto.unidade_processamento_id
        model.nome_comercial = produto.nome_comercial
        model.tipo_produto = produto.tipo_produto.value
        model.tipo_processamento = produto.tipo_processamento.value
        model.peso_liquido_kg = produto.peso_liquido_kg
        model.rendimento_percentual = produto.rendimento_percentual
        model.mercado_destino = produto.mercado_destino.value
        model.data_registro = produto.data_registro
        model.ativo = produto.ativo
        model.observacoes = produto.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, produto_id: UUID) -> ProdutoProcessado | None:
        model = await self.session.get(ProdutoProcessadoModel, produto_id)
        return self._to_domain(model) if model else None

    async def get_by_codigo(self, codigo_produto: str) -> ProdutoProcessado | None:
        stmt = select(ProdutoProcessadoModel).where(ProdutoProcessadoModel.codigo_produto == codigo_produto.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[ProdutoProcessado]:
        stmt = select(ProdutoProcessadoModel).order_by(ProdutoProcessadoModel.codigo_produto.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_unidade(self, unidade_processamento_id: UUID) -> list[ProdutoProcessado]:
        stmt = select(ProdutoProcessadoModel).where(ProdutoProcessadoModel.unidade_processamento_id == unidade_processamento_id).order_by(ProdutoProcessadoModel.codigo_produto.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo_produto: TipoProdutoProcessado) -> list[ProdutoProcessado]:
        stmt = select(ProdutoProcessadoModel).where(ProdutoProcessadoModel.tipo_produto == tipo_produto.value).order_by(ProdutoProcessadoModel.codigo_produto.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_destino(self, mercado_destino: MercadoDestino) -> list[ProdutoProcessado]:
        stmt = select(ProdutoProcessadoModel).where(ProdutoProcessadoModel.mercado_destino == mercado_destino.value).order_by(ProdutoProcessadoModel.codigo_produto.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, produto_id: UUID) -> bool:
        model = await self.session.get(ProdutoProcessadoModel, produto_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_codigo(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(ProdutoProcessadoModel).where(ProdutoProcessadoModel.codigo_produto.like(f'PRD/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'PRD/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: ProdutoProcessadoModel) -> ProdutoProcessado:
        return ProdutoProcessado(id=model.id, codigo_produto=model.codigo_produto, unidade_processamento_id=model.unidade_processamento_id, nome_comercial=model.nome_comercial, tipo_produto=TipoProdutoProcessado(model.tipo_produto), tipo_processamento=TipoProcessamento(model.tipo_processamento), peso_liquido_kg=model.peso_liquido_kg, rendimento_percentual=model.rendimento_percentual, mercado_destino=MercadoDestino(model.mercado_destino), data_registro=model.data_registro, ativo=model.ativo, observacoes=model.observacoes)