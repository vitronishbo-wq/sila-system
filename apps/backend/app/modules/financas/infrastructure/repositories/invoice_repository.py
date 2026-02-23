import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from ...domain.models.invoice import Invoice
from ...domain.models.enums import InvoiceStatus
from ..models.invoice_model import InvoiceModel

logger = logging.getLogger(__name__)


class InvoiceRepository:
    """Repositório de faturas com mapeamento entre Domínio e Persistência."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def _to_domain(self, model: InvoiceModel) -> Invoice:
        """Converte modelo de persistência para entidade de domínio."""
        return Invoice(
            id=model.id,
            citizen_id=model.citizen_id,
            reference=model.reference,
            revenue_code=model.revenue_code,
            cost_center=model.cost_center,
            service_code=model.service_code,
            service_name=model.service_name,
            amount=float(model.amount),
            due_date=model.due_date,
            request_id=model.request_id,
            currency=model.currency,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            paid_at=model.paid_at
        )

    def _to_model(self, domain: Invoice) -> InvoiceModel:
        """Converte entidade de domínio para modelo de persistência."""
        return InvoiceModel(
            id=domain.id,
            citizen_id=domain.citizen_id,
            reference=domain.reference,
            revenue_code=domain.revenue_code,
            cost_center=domain.cost_center,
            service_code=domain.service_code,
            service_name=domain.service_name,
            amount=domain.amount,
            due_date=domain.due_date,
            request_id=domain.request_id,
            currency=domain.currency,
            status=domain.status,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            paid_at=domain.paid_at
        )

    async def get_by_id(self, invoice_id: str) -> Optional[Invoice]:
        """Busca fatura por ID."""
        stmt = select(InvoiceModel).where(InvoiceModel.id == invoice_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
    
    async def create(self, invoice: Invoice) -> Invoice:
        """Persiste uma nova fatura com commit controlado."""
        model = self._to_model(invoice)
        self.db.add(model)
        await self.db.flush()
        await self.db.refresh(model)
        logger.info(f"Fatura {invoice.id} criada com sucesso")
        return self._to_domain(model)

    async def save(self, invoice: Invoice) -> Invoice:
        """Salva (cria ou atualiza) uma fatura com commit controlado."""
        stmt = select(InvoiceModel).where(InvoiceModel.id == invoice.id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            model = self._to_model(invoice)
            self.db.add(model)
            logger.info(f"Fatura {invoice.id} criada")
        else:
            model.status = invoice.status
            model.updated_at = invoice.updated_at
            model.paid_at = invoice.paid_at
            model.amount = invoice.amount
            logger.info(f"Fatura {invoice.id} atualizada")
        
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)

    async def get_by_citizen(self, citizen_id: str) -> List[Invoice]:
        """Busca todas as faturas de um cidadão."""
        stmt = (
            select(InvoiceModel)
            .where(InvoiceModel.citizen_id == citizen_id)
            .order_by(InvoiceModel.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
    
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[Invoice]:
        """Listar todas as faturas com paginação."""
        stmt = (
            select(InvoiceModel)
            .order_by(InvoiceModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def delete(self, invoice_id: str) -> bool:
        """Remove uma fatura com commit controlado."""
        stmt = select(InvoiceModel).where(InvoiceModel.id == invoice_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            self.db.delete(model)
            await self.db.flush()
            logger.info(f"Fatura {invoice_id} removida")
            return True
        return False
    
    async def get_pending(self, citizen_id: str) -> List[Invoice]:
        """Busca faturas pendentes de um cidadão."""
        stmt = (
            select(InvoiceModel).where(
                InvoiceModel.citizen_id == citizen_id,
                InvoiceModel.status == InvoiceStatus.PENDING
            )
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]