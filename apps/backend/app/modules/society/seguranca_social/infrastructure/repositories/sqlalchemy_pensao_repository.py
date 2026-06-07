from __future__ import annotations

from datetime import date

from sqlalchemy import func, select

from apps.backend.app.modules.society.seguranca_social.application.ports import PensaoRepositoryPort
from apps.backend.app.modules.society.seguranca_social.domain.enums import (
    Periodicidade,
    StatusPensao,
    TipoPensao,
)
from apps.backend.app.modules.society.seguranca_social.domain.models.pensao import Pensao
from apps.backend.app.modules.society.seguranca_social.infrastructure.models.pensao_model import (
    PensaoModel,
)


class SQLAlchemyPensaoRepository(PensaoRepositoryPort):
    def __init__(self, session):
        self.session = session

    async def save(self, pensao: Pensao) -> Pensao:
        model = await self.session.get(PensaoModel, pensao.id)
        if not model:
            model = PensaoModel(id=pensao.id)
            self.session.add(model)
        model.numero_processo = pensao.numero_processo
        model.beneficiario_id = pensao.beneficiario_id
        model.tipo = pensao.tipo.value
        model.data_inicio = pensao.data_inicio
        model.valor_mensal = pensao.valor_mensal
        model.periodicidade = pensao.periodicidade.value
        model.status = pensao.status.value
        model.data_fim = pensao.data_fim
        model.conta_bancaria = pensao.conta_bancaria
        model.iban = pensao.iban
        model.observacoes = pensao.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id):
        model = await self.session.get(PensaoModel, id)
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_processo: str):
        stmt = select(PensaoModel).where(PensaoModel.numero_processo == numero_processo)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_filtros(self, *, beneficiario_id=None, tipo=None, status=None):
        stmt = select(PensaoModel)
        if beneficiario_id:
            stmt = stmt.where(PensaoModel.beneficiario_id == beneficiario_id)
        if tipo:
            stmt = stmt.where(PensaoModel.tipo == tipo.value)
        if status:
            stmt = stmt.where(PensaoModel.status == status.value)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_numero_processo(self, ano: int) -> str:
        stmt = (
            select(func.count())
            .select_from(PensaoModel)
            .where(PensaoModel.numero_processo.like(f"PEN/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"PEN/{ano}/{count + 1:04d}"

    @staticmethod
    def _to_domain(model: PensaoModel) -> Pensao:
        return Pensao(
            id=model.id,
            numero_processo=model.numero_processo,
            beneficiario_id=model.beneficiario_id,
            tipo=TipoPensao(model.tipo),
            data_inicio=model.data_inicio or date.today(),
            valor_mensal=model.valor_mensal,
            periodicidade=Periodicidade(model.periodicidade),
            status=StatusPensao(model.status),
            data_fim=model.data_fim,
            conta_bancaria=model.conta_bancaria,
            iban=model.iban,
            observacoes=model.observacoes,
        )
