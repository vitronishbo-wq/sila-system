from dataclasses import dataclass
from uuid import UUID


@dataclass
class ResolveAuditCase:
    case_id: UUID
