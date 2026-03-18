"""Procurement command handlers."""
from datetime import datetime
import uuid
from apps.backend.app.modules.procurement.application.commands.procurement_commands import CreateTenderCommand, SubmitBidCommand, AwardContractCommand, CreateSupplierCommand
from apps.backend.app.modules.procurement.domain.models.tender import Tender
from apps.backend.app.modules.procurement.domain.models.bid import Bid
from apps.backend.app.modules.procurement.domain.models.contract import Contract
from apps.backend.app.modules.procurement.domain.models.supplier import Supplier
from apps.backend.app.modules.procurement.domain.ports.tender_repository_port import TenderRepositoryPort
from apps.backend.app.modules.procurement.domain.ports.bid_repository_port import BidRepositoryPort
from apps.backend.app.modules.procurement.domain.ports.contract_repository_port import ContractRepositoryPort
from apps.backend.app.modules.procurement.domain.ports.supplier_repository_port import SupplierRepositoryPort

class CreateTenderHandler:

    def __init__(self, tender_repo: TenderRepositoryPort):
        self.tender_repo = tender_repo

    async def handle(self, command: CreateTenderCommand) -> Tender:
        keeper = Tender(id=str(uuid.uuid4()), title=command.title, description=command.description, budget=float(command.budget), deadline=datetime.fromisoformat(command.deadline) if isinstance(command.deadline, str) else command.deadline, metadata=command.metadata or {})
        return await self.tender_repo.create(keeper)

class SubmitBidHandler:

    def __init__(self, bid_repo: BidRepositoryPort, tender_repo: TenderRepositoryPort):
        self.bid_repo = bid_repo
        self.tender_repo = tender_repo

    async def handle(self, command: SubmitBidCommand) -> Bid:
        tender = await self.tender_repo.get_by_id(command.tender_id)
        if not tender:
            raise ValueError(f'Tender {command.tender_id} not found')
        bid = Bid(id=str(uuid.uuid4()), tender_id=command.tender_id, supplier_id=command.supplier_id, amount=float(command.amount), proposal=command.proposal, metadata=command.metadata or {})
        return await self.bid_repo.create(bid)

class AwardContractHandler:

    def __init__(self, tender_repo: TenderRepositoryPort, bid_repo: BidRepositoryPort, contract_repo: ContractRepositoryPort):
        self.tender_repo = tender_repo
        self.bid_repo = bid_repo
        self.contract_repo = contract_repo

    async def handle(self, command: AwardContractCommand) -> Contract:
        tender = await self.tender_repo.get_by_id(command.tender_id)
        if not tender:
            raise ValueError(f'Tender {command.tender_id} not found')
        bid = await self.bid_repo.get_by_id(command.bid_id)
        if not bid:
            raise ValueError(f'Bid {command.bid_id} not found')
        tender.award(command.supplier_id)
        await self.tender_repo.save(tender)
        contract = Contract(id=str(uuid.uuid4()), tender_id=command.tender_id, supplier_id=command.supplier_id, amount=bid.amount, start_date=datetime.utcnow(), end_date=datetime.utcnow(), metadata=command.metadata or {})
        return await self.contract_repo.create(contract)

class CreateSupplierHandler:

    def __init__(self, supplier_repo: SupplierRepositoryPort):
        self.supplier_repo = supplier_repo

    async def handle(self, command: CreateSupplierCommand) -> Supplier:
        supplier = Supplier(id=str(uuid.uuid4()), name=command.name, tax_id=command.tax_id, contact=command.contact, metadata=command.metadata or {})
        return await self.supplier_repo.create(supplier)