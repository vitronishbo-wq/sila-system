from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestNumber:
    value: str

    @staticmethod
    def generate(sequence: Optional[int] = None) -> str:
        if sequence is not None:
            return f"REQ-{sequence:06d}"
        from uuid import uuid4
        return f"REQ-{uuid4().hex[:12]}"
