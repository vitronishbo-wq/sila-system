"""Identity domain enums."""
from enum import Enum

class IdentityStatus(Enum):
    """Identity status enumeration."""
    PENDING = 'PENDING'
    VERIFIED = 'VERIFIED'
    REJECTED = 'REJECTED'
    SUSPENDED = 'SUSPENDED'

class TrustLevel(Enum):
    """Trust level enumeration."""
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    VERIFIED = 'VERIFIED'