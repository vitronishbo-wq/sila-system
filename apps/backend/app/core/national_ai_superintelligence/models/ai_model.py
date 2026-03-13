from dataclasses import dataclass

@dataclass
class AIModel:
    name: str
    version: str
    parameters: dict