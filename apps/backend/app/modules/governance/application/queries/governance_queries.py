"""Governance domain queries."""

from dataclasses import dataclass


@dataclass
class GetWorkflowQuery:
    """Query to retrieve workflow state."""

    workflow_id: str


@dataclass
class ListWorkflowsQuery:
    """Query to list workflows."""

    filter_by: dict = None
    limit: int = 100
    offset: int = 0


@dataclass
class GetGovernanceRequestQuery:
    """Query to retrieve governance request."""

    request_id: str


@dataclass
class ListPendingApprovalsQuery:
    """Query to list pending approvals."""

    limit: int = 100
    offset: int = 0
