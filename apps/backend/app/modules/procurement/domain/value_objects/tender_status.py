from enum import StrEnum


class TenderStatus(StrEnum):
    DRAFT = "draft"
    OPEN = "open"
    EVALUATION = "evaluation"
    AWARDED = "awarded"
    CANCELLED = "cancelled"
