from uuid import UUID

from apps.backend.app.modules.society.familia.domain.exceptions.family_exceptions import (
    ExclusiveMarriageError,
)


class ExclusiveMarriageRule:
    def validate(self, *, citizen_id: UUID, active_spouse_id: UUID | None) -> bool:
        if active_spouse_id is not None:
            raise ExclusiveMarriageError(citizen_id, active_spouse_id)
        return True
