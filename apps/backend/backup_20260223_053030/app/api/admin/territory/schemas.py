"""
Schemas para Territory API
"""

from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import List, Optional


class TerritoryNode(BaseModel):
    """Nó territorial simplificado para API"""
    id: UUID
    code: Optional[str] = None
    name: str
    type: str  # "province" | "municipality" | "commune"
    parent_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


class TerritoryNodeWithChildren(TerritoryNode):
    """Nó territorial com filhos (para navegação hierárquica)"""
    children: List["TerritoryNodeWithChildren"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

