from uuid import UUID

from apps.backend.app.modules.society.familia.domain.exceptions.family_exceptions import (
    BiologicalCoherenceError,
)


class BiologicalCoherenceRule:
    def validate_parent_child_age_gap(
        self, *, parent_id: UUID, child_id: UUID, parent_age: int, child_age: int
    ) -> bool:
        if parent_age - child_age < 12:
            raise BiologicalCoherenceError(parent_id, child_id, "diferenca etaria insuficiente")
        return True
