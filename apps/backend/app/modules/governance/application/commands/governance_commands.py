"""Governance domain commands."""

from dataclasses import dataclass


@dataclass
class StartWorkflowCommand:
    """Command to start a workflow process."""

    workflow_name: str
    context: dict
    metadata: dict | None = None


@dataclass
class TransitionWorkflowCommand:
    """Command to transition workflow state."""

    workflow_id: str
    action: str
    data: dict


@dataclass
class ApproveRequestCommand:
    """Command to approve governance request."""

    request_id: str
    approver_id: str
    notes: str | None = None


@dataclass
class RejectRequestCommand:
    """Command to reject governance request."""

    request_id: str
    rejector_id: str
    reason: str
