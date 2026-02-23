from enum import Enum


class MetricSource(str, Enum):
    SERVICE_REQUESTS = "service_requests"
    WORKFLOW = "workflow"
    FINANCE = "finance"
    CITIZEN = "citizen"
