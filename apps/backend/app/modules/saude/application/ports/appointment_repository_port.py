from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class AppointmentRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, appointment_id: UUID):
        pass
