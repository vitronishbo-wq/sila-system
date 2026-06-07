from __future__ import annotations

from abc import ABC, abstractmethod


class SupplierRepository(ABC):
    @abstractmethod
    def get(self, supplier_id):
        raise NotImplementedError

    @abstractmethod
    def save(self, supplier):
        raise NotImplementedError
