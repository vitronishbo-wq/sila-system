from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class TransferRepositoryPort(ABC):
    """Porta para persistencia de registros de transferência com trilha de auditoria."""

    @abstractmethod
    async def save(self, transfer_data: dict) -> dict:
        """Salvar registro de transferência com validação de UNIQUE constraint (transfer_number)."""
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter transferência por UUID."""
        pass

    @abstractmethod
    async def get_by_transfer_number(self, transfer_number: str) -> dict | None:
        """Obter transferência por número único de processo."""
        pass

    @abstractmethod
    async def get_by_student(self, student_id: UUID) -> list[dict]:
        """Listar todas as transferências de um estudante."""
        pass

    @abstractmethod
    async def get_by_status(self, status: str) -> list[dict]:
        """Listar transferências por status (REQUESTED, IN_PROGRESS, COMPLETED, REJECTED, CANCELLED)."""
        pass

    @abstractmethod
    async def list_pending_transfers(self) -> list[dict]:
        """Listar transferências pendentes (não concluídas)."""
        pass

    @abstractmethod
    async def update_status(self, id: UUID, status: str, metadata: dict | None = None) -> dict | None:
        """Atualizar status de transferência com opcionalmente atualizar metadata."""
        pass

    @abstractmethod
    async def mark_completed(self, id: UUID, completed_at: datetime | None = None) -> dict | None:
        """Marcar transferência como concluída."""
        pass

    @abstractmethod
    async def get_student_transfer_count(self, student_id: UUID) -> int:
        """Contar quantas transferências um estudante já teve."""
        pass


from datetime import datetime
