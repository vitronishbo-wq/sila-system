"""Infrastructure Layer - Database, repositories, integrations, cache, notifications, audit"""

# Database layer
from .db import (
    TaxpayerModel,
    TaxDeclarationModel,
    TaxDebtModel,
    TaxPaymentModel,
    TaxCertificateModel,
    TaxAuditModel,
    TaxSequenceModel,
)

# Repository layer
from .repositories import (
    BaseRepository,
    TaxpayerRepository,
    DeclarationRepository,
    DebtRepository,
    PaymentRepository,
    CertificateRepository,
    AuditRepository,
)

# Integration layer
from .integrations import (
    AGTException,
    AGTTimeoutError,
    AGTAuthenticationError,
    AGTNotFoundError,
    AGTRateLimitError,
    AGTValidationError,
    AGTRateLimiter,
    AGTAPIClient,
    AGTMockClient,
    AGTWebhookHandler,
)

# Cache layer
from .cache import (
    RedisCache,
    get_cache,
    close_cache,
    CacheKeys,
    CacheMetrics,
    get_metrics,
    reset_metrics,
    report_metrics,
)

# Notification layer
from .notifications import (
    NotificationService,
    Notification,
    NotificationType,
    NotificationStatus,
    NotificationProvider,
    get_notification_service,
    EmailProvider,
    SendgridEmailProvider,
    SMSProvider,
    TwilioSMSProvider,
    AfricasTalkingSMSProvider,
    MockSMSProvider,
    PushProvider,
    FirebasePushProvider,
    OneSignalPushProvider,
    MockPushProvider,
)

# Audit layer
from .audit import (
    AuditLogger,
    AuditEntry,
    AuditAction,
    AuditLevel,
    get_audit_logger,
    AuditStorage,
    InMemoryAuditStorage,
    DatabaseAuditStorage,
    FileAuditStorage,
)

__all__ = [
    # Models
    'TaxpayerModel',
    'TaxDeclarationModel',
    'TaxDebtModel',
    'TaxPaymentModel',
    'TaxCertificateModel',
    'TaxAuditModel',
    'TaxSequenceModel',
    # Repositories
    'BaseRepository',
    'TaxpayerRepository',
    'DeclarationRepository',
    'DebtRepository',
    'PaymentRepository',
    'CertificateRepository',
    'AuditRepository',
    # Integrations
    'AGTException',
    'AGTTimeoutError',
    'AGTAuthenticationError',
    'AGTNotFoundError',
    'AGTRateLimitError',
    'AGTValidationError',
    'AGTRateLimiter',
    'AGTAPIClient',
    'AGTMockClient',
    'AGTWebhookHandler',
    # Cache
    'RedisCache',
    'get_cache',
    'close_cache',
    'CacheKeys',
    'CacheMetrics',
    'get_metrics',
    'reset_metrics',
    'report_metrics',
    # Notifications
    'NotificationService',
    'Notification',
    'NotificationType',
    'NotificationStatus',
    'NotificationProvider',
    'get_notification_service',
    'EmailProvider',
    'SendgridEmailProvider',
    'SMSProvider',
    'TwilioSMSProvider',
    'AfricasTalkingSMSProvider',
    'MockSMSProvider',
    'PushProvider',
    'FirebasePushProvider',
    'OneSignalPushProvider',
    'MockPushProvider',
    # Audit
    'AuditLogger',
    'AuditEntry',
    'AuditAction',
    'AuditLevel',
    'get_audit_logger',
    'AuditStorage',
    'InMemoryAuditStorage',
    'DatabaseAuditStorage',
    'FileAuditStorage',
]
