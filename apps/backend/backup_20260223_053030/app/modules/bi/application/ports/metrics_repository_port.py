from typing import Protocol, List, Optional


class MetricsRepositoryPort(Protocol):
    def add(self, metric):
        ...

    def list(self, limit: int = 100) -> List:
        ...

    def find_by_code(self, code: str):
        ...
