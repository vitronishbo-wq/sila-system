from enum import Enum

class TenderStatus(str, Enum):
    DRAFT = 'draft'
    OPEN = 'open'
    EVALUATION = 'evaluation'
    AWARDED = 'awarded'
    CANCELLED = 'cancelled'