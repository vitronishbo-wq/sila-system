"""
Service Requests domain enums
All values are lowercase for PostgreSQL compatibility
Canonical definitions - single source of truth
"""
from enum import Enum

class ServiceRequestStatus(str, Enum):
    """Status do pedido de serviço"""
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    UNDER_REVIEW = 'under_review'
    IN_PROGRESS = 'in_progress'
    WAITING_INFO = 'waiting_info'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

    @classmethod
    def active_statuses(cls):
        return [cls.SUBMITTED, cls.UNDER_REVIEW, cls.IN_PROGRESS, cls.WAITING_INFO]

    @classmethod
    def terminal_statuses(cls):
        return [cls.COMPLETED, cls.REJECTED, cls.CANCELLED, cls.EXPIRED]

class ServiceType(str, Enum):
    """Tipos de serviço disponíveis"""
    IDENTITY_BI = 'identity_bi'
    IDENTITY_CERTIFICATE = 'identity_certificate'
    IDENTITY_RECTIFICATION = 'identity_rectification'
    CIVIL_BIRTH = 'civil_birth'
    CIVIL_MARRIAGE = 'civil_marriage'
    CIVIL_DEATH = 'civil_death'
    HEALTH_APPOINTMENT = 'health_appointment'
    HEALTH_PRESCRIPTION = 'health_prescription'
    HEALTH_EXAM = 'health_exam'
    FINANCE_TAX = 'finance_tax'
    FINANCE_INVOICE = 'finance_invoice'
    FINANCE_PAYMENT = 'finance_payment'
    EDUCATION_ENROLLMENT = 'education_enrollment'
    EDUCATION_CERTIFICATE = 'education_certificate'
    YOUTH_PROGRAM = 'youth_program'
    EMPLOYMENT_APPLICATION = 'employment_application'
    SOCIAL_BENEFIT = 'social_benefit'
    GENERAL_COMPLAINT = 'general_complaint'
    GENERAL_SUGGESTION = 'general_suggestion'
    GENERAL_SUPPORT = 'general_support'

class RequestChannel(str, Enum):
    """Canal de origem do pedido"""
    WEB = 'web'
    MOBILE = 'mobile'
    COUNTER = 'counter'
    EMAIL = 'email'
    API = 'api'
    WHATSAPP = 'whatsapp'

class RequestPriority(str, Enum):
    """Prioridade do pedido"""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'
    CRITICAL = 'critical'

class EventType(str, Enum):
    CREATED = 'created'
    WORKFLOW_STARTED = 'workflow_started'
    STATE_CHANGED = 'state_changed'
    ATTACHMENT_ADDED = 'attachment_added'
    CLOSED = 'closed'

class RequestStatus:
    """Legacy status aliases mapping to ServiceRequestStatus"""
    RECEIVED = ServiceRequestStatus.SUBMITTED
    ACCEPTED = ServiceRequestStatus.APPROVED
    CLOSED = ServiceRequestStatus.COMPLETED
    REJECTED = ServiceRequestStatus.REJECTED
    CANCELLED = ServiceRequestStatus.CANCELLED
    DRAFT = ServiceRequestStatus.DRAFT
    UNDER_REVIEW = ServiceRequestStatus.UNDER_REVIEW