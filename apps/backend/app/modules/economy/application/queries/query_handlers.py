"""Economy query handlers."""

from apps.backend.app.modules.economy.application.queries.economy_queries import (
    GetInvoiceByIdQuery,
    ListInvoicesByCitizenQuery,
    ListPaymentsByCitizenQuery,
)


class GetInvoiceByIdHandler:
    """Handle get invoice by ID query."""

    def __init__(self, invoice_repo):
        self.invoice_repo = invoice_repo

    async def handle(self, query: GetInvoiceByIdQuery):
        """Execute query."""
        return await self.invoice_repo.get_by_id(query.invoice_id)


class ListInvoicesByCitizenHandler:
    """Handle list invoices for citizen query."""

    def __init__(self, invoice_repo):
        self.invoice_repo = invoice_repo

    async def handle(self, query: ListInvoicesByCitizenQuery) -> list:
        """Execute query."""
        return await self.invoice_repo.list_by_citizen(
            query.citizen_id, limit=query.limit, offset=query.offset
        )


class ListPaymentsByCitizenHandler:
    """Handle list payments for citizen query."""

    def __init__(self, payment_repo):
        self.payment_repo = payment_repo

    async def handle(self, query: ListPaymentsByCitizenQuery) -> list:
        """Execute query."""
        return await self.payment_repo.list_by_citizen(
            query.citizen_id, limit=query.limit, offset=query.offset
        )
