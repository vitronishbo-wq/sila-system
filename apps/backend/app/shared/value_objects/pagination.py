from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Pagination:
    limit: int = 100
    offset: int = 0

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise ValueError('limit must be >= 1')
        if self.offset < 0:
            raise ValueError('offset must be >= 0')