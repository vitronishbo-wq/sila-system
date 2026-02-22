from dataclasses import dataclass
from uuid import UUID
from typing import Optional


@dataclass
class GetDeclarationHistoryQuery:
    """Query para buscar histórico de declarações"""
    taxpayer_id: UUID
    year: Optional[int] = None
    skip: int = 0
    limit: int = 100
