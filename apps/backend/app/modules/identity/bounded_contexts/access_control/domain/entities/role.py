from dataclasses import dataclass
from uuid import UUID


@dataclass
class Role:
    """Role entity for RBAC (Role-Based Access Control)"""

    id: UUID
    name: str
    description: str
