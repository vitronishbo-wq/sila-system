"""Procurement query handlers."""
from typing import List, Optional
from apps.backend.app.modules.procurement.application.queries.procurement_queries import GetTenderByIdQuery, ListTendersByStatusQuery, ListBidsForTenderQuery, GetSupplierByIdQuery, ListAllSuppliersQuery
from apps.backend.app.modules.procurement.domain.ports.tender_repository_port import TenderRepositoryPort
from apps.backend.app.modules.procurement.domain.ports.bid_repository_port import BidRepositoryPort
from apps.backend.app.modules.procurement.domain.ports.supplier_repository_port import SupplierRepositoryPort

class GetTenderByIdHandler:

    def __init__(self, tender_repo: TenderRepositoryPort):
        self.tender_repo = tender_repo

    async def handle(self, query: GetTenderByIdQuery):
        return await self.tender_repo.get_by_id(query.tender_id)

class ListTendersByStatusHandler:

    def __init__(self, tender_repo: TenderRepositoryPort):
        self.tender_repo = tender_repo

    async def handle(self, query: ListTendersByStatusQuery) -> List:
        return await self.tender_repo.list_by_status(query.status, limit=query.limit, offset=query.offset)

class ListBidsForTenderHandler:

    def __init__(self, bid_repo: BidRepositoryPort):
        self.bid_repo = bid_repo

    async def handle(self, query: ListBidsForTenderQuery) -> List:
        return await self.bid_repo.list_by_tender(query.tender_id, limit=query.limit, offset=query.offset)

class GetSupplierByIdHandler:

    def __init__(self, supplier_repo: SupplierRepositoryPort):
        self.supplier_repo = supplier_repo

    async def handle(self, query: GetSupplierByIdQuery):
        return await self.supplier_repo.get_by_id(query.supplier_id)

class ListAllSuppliersHandler:

    def __init__(self, supplier_repo: SupplierRepositoryPort):
        self.supplier_repo = supplier_repo

    async def handle(self, query: ListAllSuppliersQuery) -> List:
        return await self.supplier_repo.list_all(limit=query.limit, offset=query.offset)