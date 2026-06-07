from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.justice.domain.value_objects.nationality import NationalityMode


@dataclass
class Citizen:
    first_name: str
    last_name: str
    birth_date: date
    birth_place: str
    nationality: NationalityMode
    id: UUID = field(default_factory=uuid4)
    father_id: UUID | None = None
    mother_id: UUID | None = None
