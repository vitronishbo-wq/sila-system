from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.domain.transfer_wizard_session import (
    TransferWizardSession,
    TransferWizardStatus,
)
from apps.backend.app.modules.educacao.infrastructure.models.transfer_wizard_model import (
    TransferWizardModel,
)


class TransferWizardRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _to_domain(model: TransferWizardModel) -> TransferWizardSession:
        return TransferWizardSession(
            id=model.id,
            citizen_id=model.citizen_id,
            status=TransferWizardStatus(model.status),
            passo_atual=model.passo_atual,
            origem_escola_id=model.origem_escola_id,
            origem_turma_id=model.origem_turma_id,
            origem_classe=model.origem_classe,
            destino_escola_id=model.destino_escola_id,
            destino_turma_id=model.destino_turma_id,
            destino_classe=model.destino_classe,
            destino_turno=model.destino_turno,
            motivo=model.motivo,
            elegibilidade=model.elegibilidade,
            reserva_id=model.reserva_id,
            transferencia_id=model.transferencia_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            expires_at=model.expires_at,
        )

    async def create(self, session: TransferWizardSession) -> TransferWizardSession:
        stmt = (
            pg_insert(TransferWizardModel)
            .values(
                id=session.id,
                citizen_id=session.citizen_id,
                status=session.status.value,
                passo_atual=session.passo_atual,
                origem_escola_id=session.origem_escola_id,
                origem_turma_id=session.origem_turma_id,
                origem_classe=session.origem_classe,
                destino_escola_id=session.destino_escola_id,
                destino_turma_id=session.destino_turma_id,
                destino_classe=session.destino_classe,
                destino_turno=session.destino_turno,
                motivo=session.motivo,
                elegibilidade=session.elegibilidade,
                reserva_id=session.reserva_id,
                transferencia_id=session.transferencia_id,
                created_at=session.created_at,
                updated_at=session.updated_at,
                expires_at=session.expires_at,
            )
            .returning(TransferWizardModel)
        )
        result = await self._session.execute(stmt)
        return self._to_domain(result.scalar_one())

    async def get_by_id(self, wizard_id: uuid.UUID) -> Optional[TransferWizardSession]:
        stmt = select(TransferWizardModel).where(TransferWizardModel.id == wizard_id)
        model = await self._session.execute(stmt)
        model = model.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def list_by_citizen(self, citizen_id: uuid.UUID) -> list[TransferWizardSession]:
        stmt = (
            select(TransferWizardModel)
            .where(TransferWizardModel.citizen_id == citizen_id)
            .order_by(TransferWizardModel.created_at.desc())
        )
        models = await self._session.execute(stmt)
        return [self._to_domain(m) for m in models.scalars().all()]

    async def save(self, session: TransferWizardSession) -> None:
        stmt = (
            pg_insert(TransferWizardModel)
            .values(
                id=session.id,
                citizen_id=session.citizen_id,
                status=session.status.value,
                passo_atual=session.passo_atual,
                origem_escola_id=session.origem_escola_id,
                origem_turma_id=session.origem_turma_id,
                origem_classe=session.origem_classe,
                destino_escola_id=session.destino_escola_id,
                destino_turma_id=session.destino_turma_id,
                destino_classe=session.destino_classe,
                destino_turno=session.destino_turno,
                motivo=session.motivo,
                elegibilidade=session.elegibilidade,
                reserva_id=session.reserva_id,
                transferencia_id=session.transferencia_id,
                updated_at=datetime.now(timezone.utc),
                expires_at=session.expires_at,
            )
            .on_conflict_do_update(
                constraint="educacao_transfer_wizard_pkey",
                set_={
                    "status": session.status.value,
                    "passo_atual": session.passo_atual,
                    "origem_escola_id": session.origem_escola_id,
                    "origem_turma_id": session.origem_turma_id,
                    "origem_classe": session.origem_classe,
                    "destino_escola_id": session.destino_escola_id,
                    "destino_turma_id": session.destino_turma_id,
                    "destino_classe": session.destino_classe,
                    "destino_turno": session.destino_turno,
                    "motivo": session.motivo,
                    "elegibilidade": session.elegibilidade,
                    "reserva_id": session.reserva_id,
                    "transferencia_id": session.transferencia_id,
                    "updated_at": datetime.now(timezone.utc),
                    "expires_at": session.expires_at,
                },
            )
        )
        await self._session.execute(stmt)
