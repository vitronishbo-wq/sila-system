from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FamilyCode:
    value: str

    def __post_init__(self) -> None:
        if not re.match("^FAM-\\d{4}-\\d{6}$", self.value):
            raise ValueError(f"Codigo familiar invalido: {self.value}")

    @classmethod
    def generate(cls, *, year: int, sequence: int) -> FamilyCode:
        return cls(f"FAM-{year}-{sequence:06d}")
