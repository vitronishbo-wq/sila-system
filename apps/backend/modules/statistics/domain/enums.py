"""Statistics domain enums - lowercase values"""

from enum import Enum


class AggregationMethod(str, Enum):
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    RATE = "rate"
