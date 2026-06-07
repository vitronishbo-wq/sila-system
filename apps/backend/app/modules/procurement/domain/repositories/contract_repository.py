from __future__ import annotations

from abc import ABC, abstractmethod


class ContractRepository(ABC):
    @abstractmethod
    def get(self, contract_id):
        raise NotImplementedError

    @abstractmethod
    def save(self, contract):
        raise NotImplementedError
