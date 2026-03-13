from enum import Enum

class CitizenStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    SUSPENDED = 'SUSPENDED'
    DECEASED = 'DECEASED'
__all__ = ['CitizenStatus']