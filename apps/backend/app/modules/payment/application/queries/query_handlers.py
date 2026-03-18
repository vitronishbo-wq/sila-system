"""Payment query handlers."""
from typing import List, Optional
from apps.backend.app.modules.payment.application.queries.payment_queries import GetPaymentByIdQuery, GetPaymentByReferenceQuery, ListPaymentsByCitizenQuery, ListPaymentsByStatusQuery, ListAllPaymentsQuery
from apps.backend.app.modules.payment.domain.models.payment import Payment
from apps.backend.app.modules.payment.domain.ports.payment_repository_port import PaymentRepositoryPort

class GetPaymentByIdHandler:
    """Handle get payment by ID query."""

    def __init__(self, repository: PaymentRepositoryPort):
        self.repository = repository

    async def handle(self, query: GetPaymentByIdQuery) -> Optional[Payment]:
        """Execute query."""
        return await self.repository.get_by_id(query.payment_id)

class GetPaymentByReferenceHandler:
    """Handle get payment by reference query."""

    def __init__(self, repository: PaymentRepositoryPort):
        self.repository = repository

    async def handle(self, query: GetPaymentByReferenceQuery) -> Optional[Payment]:
        """Execute query."""
        return await self.repository.get_by_reference(query.reference)

class ListPaymentsByCitizenHandler:
    """Handle list payments for citizen query."""

    def __init__(self, repository: PaymentRepositoryPort):
        self.repository = repository

    async def handle(self, query: ListPaymentsByCitizenQuery) -> List[Payment]:
        """Execute query."""
        return await self.repository.list_by_citizen(query.citizen_id, limit=query.limit, offset=query.offset)

class ListPaymentsByStatusHandler:
    """Handle list payments by status query."""

    def __init__(self, repository: PaymentRepositoryPort):
        self.repository = repository

    async def handle(self, query: ListPaymentsByStatusQuery) -> List[Payment]:
        """Execute query."""
        return await self.repository.list_by_status(query.status, limit=query.limit, offset=query.offset)

class ListAllPaymentsHandler:
    """Handle list all payments query."""

    def __init__(self, repository: PaymentRepositoryPort):
        self.repository = repository

    async def handle(self, query: ListAllPaymentsQuery) -> List[Payment]:
        """Execute query."""
        return await self.repository.list_all(limit=query.limit, offset=query.offset)