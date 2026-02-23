import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ...domain.models.payment import Payment
from ..models.payment_model import PaymentModel

logger = logging.getLogger(__name__)


class PaymentRepository:
    """Repositório de pagamentos com mapeamento entre Domínio e Persistência."""
    
    def __init__(self, db: AsyncSession):
        self.db = db

    def _to_domain(self, model: PaymentModel) -> Payment:
        """Converte modelo de persistência para entidade de domínio."""
        return Payment(
            id=model.id,
            invoice_id=model.invoice_id,
            citizen_id=model.citizen_id,
            amount=float(model.amount),
            gateway_reference=model.gateway_reference,
            payment_method=model.payment_method,
            currency=model.currency,
            status=model.status,
            created_at=model.created_at,
            confirmed_at=model.confirmed_at
        )

    def _to_model(self, domain: Payment) -> PaymentModel:
        """Converte entidade de domínio para modelo de persistência."""
        return PaymentModel(
            id=domain.id,
            invoice_id=domain.invoice_id,
            citizen_id=domain.citizen_id,
            amount=domain.amount,
            gateway_reference=domain.gateway_reference,
            payment_method=domain.payment_method,
            currency=domain.currency,
            status=domain.status,
            created_at=domain.created_at,
            confirmed_at=domain.confirmed_at
        )

    async def create(self, payment: Payment) -> Payment:
        """Persiste um novo pagamento com commit controlado."""
        try:
            model = self._to_model(payment)
            self.db.add(model)
            await self.db.flush()
            await self.db.refresh(model)
            logger.info(f"Pagamento {payment.id} registado para a fatura {payment.invoice_id}")
            return self._to_domain(model)
        except Exception as e:
            logger.error(f"Erro ao persistir pagamento {payment.id}: {str(e)}")
            raise

    async def get_by_id(self, payment_id: str) -> Optional[Payment]:
        """Busca pagamento por ID."""
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_by_gateway_ref(self, gateway_reference: str) -> Optional[Payment]:
        """Busca pagamento pela referência do gateway."""
        stmt = select(PaymentModel).where(PaymentModel.gateway_reference == gateway_reference)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def exists_by_gateway_ref(self, gateway_reference: str) -> bool:
        """Verifica se existe pagamento com a referência informada."""
        stmt = select(func.count(PaymentModel.id)).where(
            PaymentModel.gateway_reference == gateway_reference
        )
        result = await self.db.execute(stmt)
        count = result.scalar()
        return (count or 0) > 0

    async def list_by_invoice(self, invoice_id: str) -> List[Payment]:
        """Lista pagamentos de uma fatura."""
        stmt = (
            select(PaymentModel)
            .where(PaymentModel.invoice_id == invoice_id)
            .order_by(PaymentModel.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_by_citizen(self, citizen_id: str) -> List[Payment]:
        """Busca pagamentos de um cidadão."""
        stmt = (
            select(PaymentModel)
            .where(PaymentModel.citizen_id == citizen_id)
            .order_by(PaymentModel.created_at.desc())
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def save(self, payment: Payment) -> Payment:
        """Salva (cria ou atualiza) um pagamento com commit controlado."""
        stmt = select(PaymentModel).where(PaymentModel.id == payment.id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            model = self._to_model(payment)
            self.db.add(model)
            logger.info(f"Pagamento {payment.id} criado")
        else:
            model.status = payment.status
            model.confirmed_at = payment.confirmed_at
            logger.info(f"Pagamento {payment.id} atualizado")
        
        await self.db.flush()
        await self.db.refresh(model)
        return self._to_domain(model)

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[Payment]:
        """Lista todos os pagamentos com paginação."""
        stmt = (
            select(PaymentModel)
            .order_by(PaymentModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def delete(self, payment_id: str) -> bool:
        """Remove um pagamento com commit controlado."""
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id)
        result = await self.db.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model:
            self.db.delete(model)
            await self.db.flush()
            logger.info(f"Pagamento {payment_id} removido")
            return True
        return False