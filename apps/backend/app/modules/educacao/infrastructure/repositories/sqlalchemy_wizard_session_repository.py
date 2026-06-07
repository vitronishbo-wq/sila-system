from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.ports.wizard_session_repository_port import (
    WizardSessionRepositoryPort,
)
from apps.backend.app.modules.educacao.domain.wizard_session import (
    WizardSession,
    WizardStatus,
)
from apps.backend.app.modules.educacao.infrastructure.models.wizard_session_model import (
    WizardSessionModel,
)


class SQLAlchemyWizardSessionRepository(WizardSessionRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, session: WizardSession) -> WizardSession:
        model = await self._to_model(session)
        await self.session.merge(model)
        await self.session.flush()
        return session

    async def get_by_id(self, session_id: UUID) -> WizardSession | None:
        model = await self.session.get(WizardSessionModel, session_id)
        if model is None:
            return None
        return self._to_domain(model)

    async def get_active_by_citizen(
        self, citizen_id: UUID
    ) -> list[WizardSession]:
        stmt = (
            select(WizardSessionModel)
            .where(
                WizardSessionModel.citizen_id == citizen_id,
                WizardSessionModel.status == WizardStatus.EM_CURSO.value,
            )
            .order_by(WizardSessionModel.created_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(m) for m in models]

    async def expire_stale(self) -> int:
        from datetime import datetime

        from sqlalchemy import update

        stmt = (
            update(WizardSessionModel)
            .where(
                WizardSessionModel.expires_at < datetime.utcnow(),
                WizardSessionModel.status == WizardStatus.EM_CURSO.value,
            )
            .values(status=WizardStatus.EXPIRADO.value)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

    async def _to_model(
        self, domain: WizardSession
    ) -> WizardSessionModel:
        model = WizardSessionModel(
            id=domain.id,
            citizen_id=domain.citizen_id,
            status=domain.status.value if domain.status else WizardStatus.EM_CURSO.value,
            passo_atual=domain.passo_atual,
            dados_estudante=domain.dados_estudante,
            dados_encarregado=domain.dados_encarregado,
            selecao_escola=domain.selecao_escola,
            documentos=domain.documentos,
            resultado_elegibilidade=domain.resultado_elegibilidade,
            pagamento=domain.pagamento,
            matricula_id=domain.matricula_id,
            expires_at=domain.expires_at,
        )
        return model

    @staticmethod
    def _to_domain(model: WizardSessionModel) -> WizardSession:
        return WizardSession(
            id=model.id,
            citizen_id=model.citizen_id,
            status=WizardStatus(model.status),
            passo_atual=model.passo_atual,
            dados_estudante=model.dados_estudante,
            dados_encarregado=model.dados_encarregado,
            selecao_escola=model.selecao_escola,
            documentos=model.documentos,
            resultado_elegibilidade=model.resultado_elegibilidade,
            pagamento=model.pagamento,
            matricula_id=model.matricula_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            expires_at=model.expires_at,
        )
