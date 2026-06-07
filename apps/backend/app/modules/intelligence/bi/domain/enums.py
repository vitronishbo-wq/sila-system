from enum import StrEnum


class MetricSource(StrEnum):
    SERVICE_REQUESTS = "service_requests"
    WORKFLOW = "workflow"
    FINANCE = "finance"
    CITIZEN = "citizen"
