"""Ports (Interface Contracts) para a camada de Aplicação."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.enums import PaymentStatus
from ...domain.models import Invoice, Payment


class PaymentRepositoryPort(ABC):
    """Port: Contrato de persistência para Payment."""

    @abstractmethod
    async def create(self, payment: Payment) -> Payment:
        """Cria um novo pagamento."""
        pass

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        """Salva/atualiza um pagamento existente."""
        pass

    @abstractmethod
    async def get_by_id(self, payment_id: str) -> Payment | None:
        """Recupera pagamento por ID."""
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: str) -> list[Payment]:
        """Lista pagamentos de um cidadão."""
        pass

    @abstractmethod
    async def list_by_invoice(self, invoice_id: str) -> list[Payment]:
        """Lista pagamentos associados a uma fatura."""
        pass

    @abstractmethod
    async def get_by_gateway_ref(self, gateway_reference: str) -> Payment | None:
        """Recupera pagamento por referência de gateway (idempotência)."""
        pass

    @abstractmethod
    async def exists_by_gateway_ref(self, gateway_reference: str) -> bool:
        """Verifica se pagamento com gateway_reference existe."""
        pass

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Payment]:
        """Lista todos os pagamentos com paginação."""
        pass

    @abstractmethod
    async def delete(self, payment_id: str) -> bool:
        """Deleta um pagamento."""
        pass


class InvoiceRepositoryPort(ABC):
    """Port: Contrato de persistência para Invoice (Fatura)."""

    @abstractmethod
    async def get_by_id(self, invoice_id: str) -> Invoice | None:
        """Recupera fatura por ID."""
        pass

    @abstractmethod
    async def save(self, invoice: Invoice) -> Invoice:
        """Salva/atualiza uma fatura."""
        pass

    @abstractmethod
    async def get_by_citizen(self, citizen_id: str) -> list[Invoice]:
        """Lista faturas de um cidadão."""
        pass

    @abstractmethod
    async def list_by_status(self, status: str) -> list[Invoice]:
        """Lista faturas por status."""
        pass


class EducacaoServicePort(ABC):
    """Port: Contrato de integração com módulo Educacao."""

    @abstractmethod
    async def registrar_pagamento_propina(
        self, reference_id: str, payment_id: str, amount: float
    ) -> None:
        """Registra pagamento de propina na educacao."""
        pass


class JuventudeServicePort(ABC):
    """Port: Contrato de integração com módulo Juventude."""

    @abstractmethod
    async def registrar_pagamento_bolsa(
        self, reference_id: str, payment_id: str, amount: float
    ) -> None:
        """Registra pagamento de bolsa na juventude."""
        pass


class EmpregoServicePort(ABC):
    """Port: Contrato de integração com módulo Emprego."""

    @abstractmethod
    async def registrar_pagamento_salario(
        self, reference_id: str, payment_id: str, amount: float
    ) -> None:
        """Registra pagamento de salário no emprego."""
        pass


class SaudeServicePort(ABC):
    """Port: Contrato de integração com módulo Saude."""

    @abstractmethod
    async def registrar_pagamento_servico(
        self, reference_id: str, payment_id: str, amount: float
    ) -> None:
        """Registra pagamento de serviço na saude."""
        pass


class AssistenciaSocialServicePort(ABC):
    """Port: Contrato de integração com módulo Assistencia Social."""

    @abstractmethod
    async def registrar_pagamento_beneficio(
        self, reference_id: str, payment_id: str, amount: float
    ) -> None:
        """Registra pagamento de benefício na assistencia social."""
        pass


class ServiceRequestsServicePort(ABC):
    """Port: Contrato de integração com módulo Service Requests."""

    @abstractmethod
    async def registrar_pagamento_taxa(
        self, reference_id: str, payment_id: str, amount: float
    ) -> None:
        """Registra pagamento de taxa nos pedidos de serviço."""
        pass


__all__ = [
    "PaymentRepositoryPort",
    "InvoiceRepositoryPort",
    "EducacaoServicePort",
    "JuventudeServicePort",
    "EmpregoServicePort",
    "SaudeServicePort",
    "AssistenciaSocialServicePort",
    "ServiceRequestsServicePort",
]
