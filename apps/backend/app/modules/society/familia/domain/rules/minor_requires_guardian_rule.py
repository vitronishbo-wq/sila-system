from uuid import UUID

from apps.backend.app.modules.society.familia.domain.exceptions.family_exceptions import (
    MinorRequiresGuardianError,
)


class MinorRequiresGuardianRule:
    def validate(self, *, minor_id: UUID, has_guardian: bool) -> bool:
        if not has_guardian:
            raise MinorRequiresGuardianError(minor_id)
        return True
