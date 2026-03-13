from uuid import uuid4
import pytest
from app.modules.society.familia.domain.exceptions.family_exceptions import MinorRequiresGuardianError
from app.modules.society.familia.domain.rules.minor_requires_guardian_rule import MinorRequiresGuardianRule

def test_minor_requires_guardian_rule() -> None:
    rule = MinorRequiresGuardianRule()
    with pytest.raises(MinorRequiresGuardianError):
        rule.validate(minor_id=uuid4(), has_guardian=False)