from __future__ import annotations

from abc import ABC, abstractmethod


class AuditCaseRepository(ABC):
    @abstractmethod
    def open_case(self, alert):
        raise NotImplementedError

    @abstractmethod
    def list_cases(self):
        raise NotImplementedError
