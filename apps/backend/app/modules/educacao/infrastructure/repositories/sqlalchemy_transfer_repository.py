from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.application.ports import TransferRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.transfer_model import TransferModel


class SQLAlchemyTransferRepository(TransferRepositoryPort):
    """Repositório real para TransferModel com trilha de auditoria e transações ACID."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, transfer_data: dict) -> dict:
        """Salvar registro de transferência com validação de UNIQUE constraint (transfer_number)."""
        model = await self.session.get(TransferModel, transfer_data.get("id"))
        if not model:
            model = TransferModel(id=transfer_data.get("id"))
            self.session.add(model)

        model.transfer_number = transfer_data.get("transfer_number")
        model.academic_identity_id = transfer_data.get("academic_identity_id")
        model.from_institution_id = transfer_data.get("from_institution_id")
        model.to_institution_id = transfer_data.get("to_institution_id")
        model.status = transfer_data.get("status", "REQUESTED")
        model.requested_at = transfer_data.get("requested_at", datetime.now(datetime.UTC))
        model.completed_at = transfer_data.get("completed_at")
        model.reason = transfer_data.get("reason")
        model.metadata_json = transfer_data.get("metadata_json", {})

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter transferência por UUID."""
        model = await self.session.get(TransferModel, id)
        return self._to_dict(model) if model else None

    async def get_by_transfer_number(self, transfer_number: str) -> dict | None:
        """Obter transferência por número único de processo."""
        stmt = select(TransferModel).where(TransferModel.transfer_number == transfer_number)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_dict(model) if model else None

    async def get_by_student(self, student_id: UUID) -> list[dict]:
        """Listar todas as transferências de um estudante."""
        stmt = select(TransferModel).where(TransferModel.academic_identity_id == student_id)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def get_by_status(self, status: str) -> list[dict]:
        """Listar transferências por status (REQUESTED, IN_PROGRESS, COMPLETED, REJECTED, CANCELLED)."""
        stmt = select(TransferModel).where(TransferModel.status == status)
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def list_pending_transfers(self) -> list[dict]:
        """Listar transferências pendentes (não concluídas)."""
        stmt = select(TransferModel).where(
            TransferModel.status.in_(["REQUESTED", "IN_PROGRESS"])
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def update_status(self, id: UUID, status: str, metadata: dict | None = None) -> dict | None:
        """Atualizar status de transferência com opcionalmente atualizar metadata."""
        model = await self.session.get(TransferModel, id)
        if not model:
            return None

        model.status = status
        if metadata:
            model.metadata_json = {**(model.metadata_json or {}), **metadata}

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def mark_completed(self, id: UUID, completed_at: datetime | None = None) -> dict | None:
        """Marcar transferência como concluída."""
        model = await self.session.get(TransferModel, id)
        if not model:
            return None

        model.status = "COMPLETED"
        model.completed_at = completed_at or datetime.now(datetime.UTC)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def get_student_transfer_count(self, student_id: UUID) -> int:
        """Contar quantas transferências um estudante já teve."""
        stmt = (
            select(TransferModel)
            .where(TransferModel.academic_identity_id == student_id)
            .where(TransferModel.status.in_(["COMPLETED", "IN_PROGRESS"]))
        )
        count = (await self.session.execute(stmt)).scalars().all()
        return len(count)

    def _to_dict(self, model: TransferModel | None) -> dict | None:
        """Converter modelo SQLAlchemy para dict."""
        if not model:
            return None
        return {
            "id": model.id,
            "transfer_number": model.transfer_number,
            "academic_identity_id": model.academic_identity_id,
            "from_institution_id": model.from_institution_id,
            "to_institution_id": model.to_institution_id,
            "status": model.status,
            "requested_at": model.requested_at,
            "completed_at": model.completed_at,
            "reason": model.reason,
            "metadata_json": model.metadata_json,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
