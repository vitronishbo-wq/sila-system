from dataclasses import dataclass

@dataclass
class DomainEntity:
    """Base class for concrete domain entities."""
    id: str