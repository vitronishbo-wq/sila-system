"""
Resources Module Event Handlers
Handlers that process natural resources domain events.
"""
import logging
from typing import Awaitable, Callable
from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.modules.resources.domain.events import ResourceExplorationLicenseApplied, ExploitationLicenseIssued, ResourceMonitoringReportFiled, ResourceLicenseStatusChanged, EnvironmentalImpactAssessmentApproved
logger = logging.getLogger(__name__)

async def handle_resource_exploration_license_applied(event: ResourceExplorationLicenseApplied) -> None:
    """Handler for ResourceExplorationLicenseApplied events."""
    logger.info(f'Exploration license applied for {event.resource_type} at {event.location}')
    pass

async def handle_exploitation_license_issued(event: ExploitationLicenseIssued) -> None:
    """Handler for ExploitationLicenseIssued events (ACAO compliance)."""
    logger.info(f'Exploitation license {event.aggregate_id} issued')
    pass

async def handle_resource_monitoring_report_filed(event: ResourceMonitoringReportFiled) -> None:
    """Handler for ResourceMonitoringReportFiled events (ACAO compliance)."""
    logger.info(f'Monitoring report filed for license {event.aggregate_id}')
    pass

async def handle_resource_license_status_changed(event: ResourceLicenseStatusChanged) -> None:
    """Handler for ResourceLicenseStatusChanged events."""
    logger.info(f'License status changed: {event.old_status} -> {event.new_status}')
    pass

async def handle_eia_approved(event: EnvironmentalImpactAssessmentApproved) -> None:
    """Handler for EnvironmentalImpactAssessmentApproved events (ACAO compliance)."""
    logger.info(f'EIA approved for project {event.aggregate_id}')
    pass
RESOURCES_EVENT_HANDLERS: dict[str, Callable[[DomainEvent], Awaitable[None]]] = {'ResourceExplorationLicenseApplied': handle_resource_exploration_license_applied, 'ExploitationLicenseIssued': handle_exploitation_license_issued, 'ResourceMonitoringReportFiled': handle_resource_monitoring_report_filed, 'ResourceLicenseStatusChanged': handle_resource_license_status_changed, 'EnvironmentalImpactAssessmentApproved': handle_eia_approved}