from uuid import uuid4
import pytest
from apps.backend.app.modules.society.familia.domain.exceptions.family_exceptions import BiologicalCoherenceError
from apps.backend.app.modules.society.familia.domain.rules.biological_coherence_rule import BiologicalCoherenceRule

def test_biological_coherence_rejects_small_age_gap() -> None:
    rule = BiologicalCoherenceRule()
    with pytest.raises(BiologicalCoherenceError):
        rule.validate_parent_child_age_gap(parent_id=uuid4(), child_id=uuid4(), parent_age=20, child_age=12)