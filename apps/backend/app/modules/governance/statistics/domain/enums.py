"""Statistics domain enums - lowercase values"""

from enum import StrEnum


class AggregationMethod(StrEnum):
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    RATE = "rate"
