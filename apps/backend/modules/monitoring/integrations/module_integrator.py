"""Module integrator for monitoring integration with other SILA modules."""

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from ..models.alert import AlertCategory, AlertSeverity, AlertType
from ..models.audit_log import AuditAction
from ..models.system_metric import MetricCategory, MetricType, MetricUnit
from ..services.alert_service import AlertService
from ..services.audit_service import AuditService
from ..services.metric_service import MetricService


class ModuleIntegrator:
    """Integration service for monitoring other SILA system modules."""

    def __init__(self, db: Session):
        self.db = db
        self.audit_service = AuditService(db)
        self.metric_service = MetricService(db)
        self.alert_service = AlertService(db)

    # ============================================================================
    # CITIZENSHIP MODULE INTEGRATION
    # ============================================================================

    def log_citizen_registration(
        self,
        user_id: int,
        citizen_id: int,
        success: bool = True,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None,
        ip_address: Optional[str] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Log citizen registration activity."""
        return self.audit_service.log_user_action(
            user_id=user_id,
            user_email=None,
            user_role=None,
            action=AuditAction.CREATE,
            module="citizenship",
            description=f"Citizen registration {'completed' if success else 'failed'}",
            resource_type="citizen",
            resource_id=citizen_id,
            ip_address=ip_address,
            province=province,
            municipality=municipality,
            success=success,
            error_message=error_message,
            duration_ms=duration_ms,
            additional_data={"operation": "citizen_registration"},
        )

    def record_document_request_metric(
        self,
        document_type: str,
        processing_time_ms: int,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Record document request processing time metric."""
        return self.metric_service.record_metric(
            metric_name=f"document_request_{document_type}",
            metric_type=MetricType.DOCUMENT_REQUESTS,
            category=MetricCategory.BUSINESS,
            value=1,
            unit=MetricUnit.COUNT,
            module="citizenship",
            component="document_service",
            province=province,
            municipality=municipality,
            metadata={
                "document_type": document_type,
                "processing_time_ms": processing_time_ms,
            },
        )

    # ============================================================================
    # HEALTH MODULE INTEGRATION
    # ============================================================================

    def log_appointment_booking(
        self,
        user_id: int,
        appointment_id: int,
        health_facility: str,
        success: bool = True,
        error_message: Optional[str] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Log health appointment booking."""
        return self.audit_service.log_user_action(
            user_id=user_id,
            user_email=None,
            user_role=None,
            action=AuditAction.CREATE,
            module="health",
            description=f"Health appointment booking at {health_facility}",
            resource_type="appointment",
            resource_id=appointment_id,
            province=province,
            municipality=municipality,
            success=success,
            error_message=error_message,
            additional_data={
                "operation": "appointment_booking",
                "facility": health_facility,
            },
        )

    def record_health_service_usage(
        self,
        service_type: str,
        facility_name: str,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Record health service usage metrics."""
        return self.metric_service.record_metric(
            metric_name=f"health_service_{service_type}",
            metric_type=MetricType.API_CALLS,
            category=MetricCategory.BUSINESS,
            value=1,
            unit=MetricUnit.COUNT,
            module="health",
            component="health_service",
            province=province,
            municipality=municipality,
            metadata={"service_type": service_type, "facility": facility_name},
        )

    # ============================================================================
    # FINANCE MODULE INTEGRATION
    # ============================================================================

    def log_payment_transaction(
        self,
        user_id: int,
        transaction_id: int,
        amount: float,
        payment_method: str,
        success: bool = True,
        error_message: Optional[str] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Log payment transaction."""
        return self.audit_service.log_user_action(
            user_id=user_id,
            user_email=None,
            user_role=None,
            action=AuditAction.CREATE if success else AuditAction.UPDATE,
            module="finance",
            description=f"Payment transaction of {amount} AOA via {payment_method}",
            resource_type="payment",
            resource_id=transaction_id,
            province=province,
            municipality=municipality,
            success=success,
            error_message=error_message,
            additional_data={
                "operation": "payment_transaction",
                "amount": amount,
                "payment_method": payment_method,
            },
        )

    def record_payment_metric(
        self,
        amount: float,
        payment_method: str,
        success: bool,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Record payment transaction metrics."""
        # Record transaction count
        self.metric_service.record_metric(
            metric_name="payment_transactions",
            metric_type=MetricType.PAYMENT_TRANSACTIONS,
            category=MetricCategory.BUSINESS,
            value=1,
            unit=MetricUnit.COUNT,
            module="finance",
            component="payment_service",
            province=province,
            municipality=municipality,
            metadata={"payment_method": payment_method, "success": success},
        )

        # Record transaction amount if successful
        if success:
            return self.metric_service.record_metric(
                metric_name="payment_amount",
                metric_type=MetricType.PAYMENT_TRANSACTIONS,
                category=MetricCategory.BUSINESS,
                value=amount,
                unit=MetricUnit.COUNT,  # Could be AOA currency unit
                module="finance",
                component="payment_service",
                province=province,
                municipality=municipality,
                metadata={"payment_method": payment_method, "currency": "AOA"},
            )

    # ============================================================================
    # JUSTICE MODULE INTEGRATION
    # ============================================================================

    def log_case_submission(
        self,
        user_id: int,
        case_id: int,
        case_type: str,
        court_name: str,
        success: bool = True,
        error_message: Optional[str] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Log justice case submission."""
        return self.audit_service.log_user_action(
            user_id=user_id,
            user_email=None,
            user_role=None,
            action=AuditAction.CREATE,
            module="justice",
            description=f"Case submission: {case_type} to {court_name}",
            resource_type="case",
            resource_id=case_id,
            province=province,
            municipality=municipality,
            success=success,
            error_message=error_message,
            additional_data={
                "operation": "case_submission",
                "case_type": case_type,
                "court": court_name,
            },
        )

    def record_case_processing_metric(
        self,
        case_type: str,
        processing_stage: str,
        duration_days: int,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Record case processing metrics."""
        return self.metric_service.record_metric(
            metric_name=f"case_processing_{processing_stage}",
            metric_type=MetricType.CASE_SUBMISSIONS,
            category=MetricCategory.BUSINESS,
            value=duration_days,
            unit=MetricUnit.COUNT,  # Days
            module="justice",
            component="case_service",
            province=province,
            municipality=municipality,
            metadata={"case_type": case_type, "processing_stage": processing_stage},
        )

    # ============================================================================
    # GOVERNANCE MODULE INTEGRATION
    # ============================================================================

    def log_governance_decision(
        self,
        user_id: int,
        decision_id: int,
        decision_type: str,
        institution: str,
        success: bool = True,
        error_message: Optional[str] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Log governance decision."""
        return self.audit_service.log_user_action(
            user_id=user_id,
            user_email=None,
            user_role=None,
            action=AuditAction.APPROVE,
            module="governance",
            description=f"Governance decision: {decision_type} by {institution}",
            resource_type="decision",
            resource_id=decision_id,
            province=province,
            municipality=municipality,
            success=success,
            error_message=error_message,
            additional_data={
                "operation": "governance_decision",
                "decision_type": decision_type,
                "institution": institution,
            },
        )

    # ============================================================================
    # COMPLAINTS MODULE INTEGRATION
    # ============================================================================

    def log_complaint_submission(
        self,
        user_id: int,
        complaint_id: int,
        complaint_type: str,
        target_institution: str,
        success: bool = True,
        error_message: Optional[str] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Log complaint submission."""
        return self.audit_service.log_user_action(
            user_id=user_id,
            user_email=None,
            user_role=None,
            action=AuditAction.CREATE,
            module="complaints",
            description=f"Complaint submission: {complaint_type} against {target_institution}",
            resource_type="complaint",
            resource_id=complaint_id,
            province=province,
            municipality=municipality,
            success=success,
            error_message=error_message,
            additional_data={
                "operation": "complaint_submission",
                "complaint_type": complaint_type,
                "target_institution": target_institution,
            },
        )

    def record_complaint_resolution_metric(
        self,
        complaint_type: str,
        resolution_time_hours: int,
        satisfaction_score: Optional[int] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Record complaint resolution metrics."""
        return self.metric_service.record_metric(
            metric_name="complaint_resolution_time",
            metric_type=MetricType.API_CALLS,  # Could be COMPLAINT_RESOLUTION
            category=MetricCategory.BUSINESS,
            value=resolution_time_hours,
            unit=MetricUnit.COUNT,  # Hours
            module="complaints",
            component="complaint_service",
            province=province,
            municipality=municipality,
            metadata={
                "complaint_type": complaint_type,
                "satisfaction_score": satisfaction_score,
            },
        )

    # ============================================================================
    # GENERIC MODULE INTEGRATION METHODS
    # ============================================================================

    def log_module_operation(
        self,
        module_name: str,
        operation: str,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None,
        additional_data: Optional[Dict[str, Any]] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Generic method to log any module operation."""
        action = self._determine_audit_action(operation)

        return self.audit_service.log_user_action(
            user_id=user_id,
            user_email=None,
            user_role=None,
            action=action,
            module=module_name,
            description=f"{module_name.title()} operation: {operation}",
            resource_type=resource_type,
            resource_id=resource_id,
            province=province,
            municipality=municipality,
            success=success,
            error_message=error_message,
            duration_ms=duration_ms,
            additional_data=additional_data or {},
        )

    def record_module_metric(
        self,
        module_name: str,
        metric_name: str,
        value: float,
        unit: MetricUnit = MetricUnit.COUNT,
        category: MetricCategory = MetricCategory.APPLICATION,
        component: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
    ):
        """Generic method to record module metrics."""
        return self.metric_service.record_metric(
            metric_name=metric_name,
            metric_type=MetricType.API_CALLS,  # Default type
            category=category,
            value=value,
            unit=unit,
            module=module_name,
            component=component or f"{module_name}_service",
            province=province,
            municipality=municipality,
            metadata=metadata,
        )

    def create_module_alert(
        self,
        module_name: str,
        alert_type: AlertType,
        title: str,
        description: str,
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        category: AlertCategory = AlertCategory.APPLICATION,
        component: Optional[str] = None,
        affected_resource_type: Optional[str] = None,
        affected_resource_id: Optional[int] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None,
    ):
        """Generic method to create module alerts."""
        from ..schemas import AlertCreate

        alert_data = AlertCreate(
            alert_type=alert_type,
            severity=severity,
            category=category,
            title=title,
            description=description,
            source_module=module_name,
            source_component=component,
            affected_resource_type=affected_resource_type,
            affected_resource_id=affected_resource_id,
            province=province,
            municipality=municipality,
            alert_data=additional_data,
        )

        return self.alert_service.create_alert(alert_data)

    def _determine_audit_action(self, operation: str) -> AuditAction:
        """Determine audit action based on operation string."""
        operation_lower = operation.lower()

        if any(
            word in operation_lower for word in ["create", "register", "submit", "add"]
        ):
            return AuditAction.CREATE
        elif any(
            word in operation_lower for word in ["update", "modify", "edit", "change"]
        ):
            return AuditAction.UPDATE
        elif any(word in operation_lower for word in ["delete", "remove", "cancel"]):
            return AuditAction.DELETE
        elif any(word in operation_lower for word in ["approve", "accept", "confirm"]):
            return AuditAction.APPROVE
        elif any(word in operation_lower for word in ["reject", "deny", "decline"]):
            return AuditAction.REJECT
        elif any(word in operation_lower for word in ["login", "signin"]):
            return AuditAction.LOGIN
        elif any(word in operation_lower for word in ["logout", "signout"]):
            return AuditAction.LOGOUT
        elif any(word in operation_lower for word in ["view", "read", "get", "fetch"]):
            return AuditAction.READ
        else:
            return AuditAction.UPDATE  # Default action
