from enum import Enum


class TaxpayerStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SUSPENDED = "suspended"
