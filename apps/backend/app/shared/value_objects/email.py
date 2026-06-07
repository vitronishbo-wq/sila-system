from __future__ import annotations

import re
from dataclasses import dataclass

EMAIL_RE = re.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not EMAIL_RE.match(self.value):
            raise ValueError(f"Invalid email: {self.value}")

    def normalized(self) -> str:
        return self.value.strip().lower()
