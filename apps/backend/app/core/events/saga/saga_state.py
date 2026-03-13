from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SagaState:
    saga_id: str
    current_step: str
    completed: bool = False