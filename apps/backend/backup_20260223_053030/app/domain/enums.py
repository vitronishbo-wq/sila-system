"""
Core domain enums - canonical definitions
All values are lowercase for PostgreSQL compatibility
All enums inherit from (str, Enum) for schema and comparison
No duplicates: single source of truth per concept
"""

from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class MaritalStatus(str, Enum):
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"
    OTHER = "other"


class CitizenStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DECEASED = "deceased"


class VerificationLevel(str, Enum):
    UNVERIFIED = "unverified"
    BASIC = "basic"
    GOVERNMENT_VERIFIED = "government_verified"
    BIOMETRIC_VERIFIED = "biometric_verified"


# Legacy aliases for backward compatibility
GenderEnum = Gender
MaritalStatusEnum = MaritalStatus
CitizenStatusEnum = CitizenStatus
VerificationLevelEnum = VerificationLevel
