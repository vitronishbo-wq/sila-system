"""Application layer do módulo taxpayer"""

from .taxpayer_application_facade import TaxpayerApplicationFacade
from .services import (
    TaxpayerService,
    TaxDeclarationService,
    TaxDebtService,
    TaxCertificateService,
    AGTSyncService,
    TaxPaymentService
)
from .commands import (
    RegisterTaxpayerCommand,
    FileDeclarationCommand,
    PayTaxCommand,
    RequestCertificateCommand
)
from .queries import (
    GetTaxpayerQuery,
    GetDeclarationHistoryQuery,
    GetTaxDebtQuery,
    GetPaymentHistoryQuery,
    GetTaxCertificateQuery
)
from .ports import (
    TaxpayerRepositoryPort,
    AGTIntegrationPort,
    NotificationPort,
    AuditPort,
    CachePort,
    EventBusPort,
    UnitOfWorkPort,
    DomainEvent
)

__all__ = [
    # Main Facade
    "TaxpayerApplicationFacade",
    # Services
    "TaxpayerService",
    "TaxDeclarationService",
    "TaxDebtService",
    "TaxCertificateService",
    "AGTSyncService",
    "TaxPaymentService",
    # Commands
    "RegisterTaxpayerCommand",
    "FileDeclarationCommand",
    "PayTaxCommand",
    "RequestCertificateCommand",
    # Queries
    "GetTaxpayerQuery",
    "GetDeclarationHistoryQuery",
    "GetTaxDebtQuery",
    "GetPaymentHistoryQuery",
    "GetTaxCertificateQuery",
    # Ports
    "TaxpayerRepositoryPort",
    "AGTIntegrationPort",
    "NotificationPort",
    "AuditPort",
    "CachePort",
    "EventBusPort",
    "UnitOfWorkPort",
    "DomainEvent"
]
