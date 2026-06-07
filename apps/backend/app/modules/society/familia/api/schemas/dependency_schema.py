from datetime import date
from uuid import UUID

from pydantic import BaseModel

from apps.backend.app.modules.society.familia.domain.enums import DependencyType


class DependencySchema(BaseModel):
    id: UUID
    dependent_citizen_id: UUID
    guardian_citizen_id: UUID
    dependency_type: DependencyType
    start_date: date
    end_date: date | None = None
