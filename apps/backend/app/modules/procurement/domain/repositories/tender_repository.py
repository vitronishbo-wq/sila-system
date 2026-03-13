from __future__ import annotations
from abc import ABC, abstractmethod

class TenderRepository(ABC):

    @abstractmethod
    def get(self, tender_id):
        raise NotImplementedError

    @abstractmethod
    def save(self, tender):
        raise NotImplementedError