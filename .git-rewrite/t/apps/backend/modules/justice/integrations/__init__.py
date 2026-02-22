"""Justice module integrations."""

from .citizenship_integration import CitizenshipIntegration
from .complaints_integration import ComplaintsIntegration
from .governance_integration import GovernanceIntegration

__all__ = [
    "CitizenshipIntegration",
    "ComplaintsIntegration",
    "GovernanceIntegration",
]
