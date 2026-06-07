"""
Ports (Interface Contracts)
Define contratos obrigatórios para repositórios
"""

from .assistencia_social_service_port import AssistenciaSocialServicePort
from .educacao_service_port import EducacaoServicePort
from .emprego_service_port import EmpregoServicePort
from .identidade_service_port import IdentidadeServicePort
from .invoice_repository_port import InvoiceRepositoryPort
from .juventude_service_port import JuventudeServicePort
from .payment_repository_port import PaymentRepositoryPort
from .saude_service_port import SaudeServicePort
from .service_requests_service_port import ServiceRequestsServicePort

__all__ = [
    "InvoiceRepositoryPort",
    "PaymentRepositoryPort",
    "EducacaoServicePort",
    "JuventudeServicePort",
    "EmpregoServicePort",
    "SaudeServicePort",
    "AssistenciaSocialServicePort",
    "ServiceRequestsServicePort",
    "IdentidadeServicePort",
]
