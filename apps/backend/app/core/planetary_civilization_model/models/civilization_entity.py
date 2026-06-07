from dataclasses import dataclass


@dataclass
class CivilizationEntity:
    id: str
    type: str
    attributes: dict
