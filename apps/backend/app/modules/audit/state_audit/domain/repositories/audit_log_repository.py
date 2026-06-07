from __future__ import annotations

from abc import ABC, abstractmethod


class AuditLogRepository(ABC):
    @abstractmethod
    def save(self, event):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError
