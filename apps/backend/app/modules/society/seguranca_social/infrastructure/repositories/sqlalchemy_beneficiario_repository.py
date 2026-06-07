from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select

from apps.backend.app.modules.society.seguranca_social.application.ports import (
    BeneficiarioRepositoryPort,
)
from apps.backend.app.modules.society.seguranca_social.domain.enums import (
    EstadoBeneficiario,
    RegimeSegurancaSocial,
    TipoBeneficiario,
)
from apps.backend.app.modules.society.seguranca_social.domain.models.beneficiario import (
    Beneficiario,
)
from apps.backend.app.modules.society.seguranca_social.infrastructure.models.beneficiario_model import (
    BeneficiarioModel,
)


class SQLAlchemyBeneficiarioRepository(BeneficiarioRepositoryPort):
    def __init__(self, session):
        self.session = session

    async def save(self, beneficiario: Beneficiario) -> Beneficiario:
        model = await self.session.get(BeneficiarioModel, beneficiario.id)
        if not model:
            model = BeneficiarioModel(id=beneficiario.id)
            self.session.add(model)
        model.numero_beneficiario = beneficiario.numero_beneficiario
        model.citizen_id = beneficiario.citizen_id
        model.data_inscricao = beneficiario.data_inscricao
        model.tipo = beneficiario.tipo.value
        model.regime = beneficiario.regime.value
        model.estado = beneficiario.estado.value
        model.data_ativacao = beneficiario.data_ativacao
        model.data_suspensao = beneficiario.data_suspensao
        model.data_cancelamento = beneficiario.data_cancelamento
        model.motivo_cancelamento = beneficiario.motivo_cancelamento
        model.observacoes = beneficiario.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID):
        model = await self.session.get(BeneficiarioModel, id)
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID):
        stmt = select(BeneficiarioModel).where(BeneficiarioModel.citizen_id == citizen_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_numero(self, numero_beneficiario: str):
        stmt = select(BeneficiarioModel).where(
            BeneficiarioModel.numero_beneficiario == numero_beneficiario
        )
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_filtros(self, *, tipo=None, estado=None, regime=None):
        stmt = select(BeneficiarioModel)
        if tipo:
            stmt = stmt.where(BeneficiarioModel.tipo == tipo.value)
        if estado:
            stmt = stmt.where(BeneficiarioModel.estado == estado.value)
        if regime:
            stmt = stmt.where(BeneficiarioModel.regime == regime.value)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_numero_beneficiario(self, ano: int) -> str:
        stmt = (
            select(func.count())
            .select_from(BeneficiarioModel)
            .where(BeneficiarioModel.numero_beneficiario.like(f"BEN/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"BEN/{ano}/{count + 1:04d}"

    @staticmethod
    def _to_domain(model: BeneficiarioModel) -> Beneficiario:
        return Beneficiario(
            id=model.id,
            numero_beneficiario=model.numero_beneficiario,
            citizen_id=model.citizen_id,
            data_inscricao=model.data_inscricao or date.today(),
            tipo=TipoBeneficiario(model.tipo),
            regime=RegimeSegurancaSocial(model.regime),
            estado=EstadoBeneficiario(model.estado),
            data_ativacao=model.data_ativacao,
            data_suspensao=model.data_suspensao,
            data_cancelamento=model.data_cancelamento,
            motivo_cancelamento=model.motivo_cancelamento,
            observacoes=model.observacoes,
        )
