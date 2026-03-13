from enum import Enum

class ContractStatus(str, Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    TERMINATED = 'terminated'