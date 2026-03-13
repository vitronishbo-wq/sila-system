from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.society.familia.domain.exceptions.family_exceptions import HeadMustBeAdultError

class HeadMustBeAdultRule:

    def validate(self, *, citizen_id: UUID, age: int) -> bool:
        if age < 18:
            raise HeadMustBeAdultError(citizen_id, age)
        return True