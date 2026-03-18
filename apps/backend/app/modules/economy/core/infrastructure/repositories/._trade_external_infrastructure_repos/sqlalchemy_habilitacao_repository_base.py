from __future__ import annotations
from typing import Generic, TypeVar
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.economy.trade.external.application.ports import HabilitacaoRepositoryPortBase
from apps.backend.app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoOperador, TipoPessoa
from apps.backend.app.modules.economy.trade.external.domain.models import HabilitacaoBase
from apps.backend.app.modules.economy.trade.external.infrastructure.models.habilitacao_columns_mixin import HabilitacaoColumnsMixin
THabilitacao = TypeVar('THabilitacao', bound=HabilitacaoBase)
THabilitacaoModel = TypeVar('THabilitacaoModel', bound=HabilitacaoColumnsMixin)

class SQLAlchemyHabilitacaoRepositoryBase(HabilitacaoRepositoryPortBase[THabilitacao], Generic[THabilitacao, THabilitacaoModel]):

    def __init__(self, session: AsyncSession, *, model_cls: type[THabilitacaoModel], domain_cls: type[THabilitacao]) -> None:
        self.session = session
        self._model_cls = model_cls
        self._domain_cls = domain_cls

    async def save(self, habilitacao: THabilitacao) -> THabilitacao:
        model = await self.session.get(self._model_cls, habilitacao.id)
        if not model:
            model = self._model_cls(id=habilitacao.id)
            self.session.add(model)
        model.tipo_operador = habilitacao.tipo_operador.value
        model.tipo_pessoa = habilitacao.tipo_pessoa.value
        model.status = habilitacao.status.value
        model.razao_social = habilitacao.razao_social
        model.cnpj_cpf = habilitacao.cnpj_cpf
        model.numero_processo = habilitacao.numero_processo
        model.data_solicitacao = habilitacao.data_solicitacao
        model.data_analise = habilitacao.data_analise
        model.data_validade = habilitacao.data_validade
        model.numero_radar = habilitacao.numero_radar
        model.motivo = habilitacao.motivo
        model.observacoes = habilitacao.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> THabilitacao | None:
        model = await self.session.get(self._model_cls, id)
        return self._to_domain(model) if model else None

    async def get_by_numero_processo(self, numero_processo: str) -> THabilitacao | None:
        stmt = select(self._model_cls).where(self._model_cls.numero_processo == numero_processo.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusHabilitacao | None=None) -> list[THabilitacao]:
        stmt = select(self._model_cls)
        if status is not None:
            stmt = stmt.where(self._model_cls.status == status.value)
        stmt = stmt.order_by(self._model_cls.data_solicitacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    def _to_domain(self, model: THabilitacaoModel) -> THabilitacao:
        return self._domain_cls(id=model.id, tipo_operador=TipoOperador(model.tipo_operador), tipo_pessoa=TipoPessoa(model.tipo_pessoa), status=StatusHabilitacao(model.status), razao_social=model.razao_social, cnpj_cpf=model.cnpj_cpf, numero_processo=model.numero_processo, data_solicitacao=model.data_solicitacao, data_analise=model.data_analise, data_validade=model.data_validade, numero_radar=model.numero_radar, motivo=model.motivo, observacoes=model.observacoes)