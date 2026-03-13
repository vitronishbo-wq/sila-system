from dataclasses import dataclass

@dataclass
class TenderDTO:
    id: str
    title: str
    status: str