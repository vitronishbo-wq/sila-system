"""
Repositório de BI - Módulo Identidade Civil

Responsabilidade: Persistência assíncrona de Bilhetes de Identidade.
Implementação robusta com SQLAlchemy, auditoria e versionamento.
"""
import uuid
import logging
from typing import Optional, List
from datetime import date

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identidade_civil.domain.models.bi_record import BIRecord
from app.modules.identidade_civil.exceptions import NotFoundException

logger = logging.getLogger("identidade_civil.repository.bi")


class BIRepository:
    """
    Repositório assíncrono para entidade BI.
    
    Persiste registros de Bilhetes de Identidade com rastreamento de versão
    e auditoria completa.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, bi_record: BIRecord) -> BIRecord:
        """Persiste ou atualiza um BI."""
        if bi_record.id:
            existing = await self.get_by_id(bi_record.id)
            if existing:
                bi_record.version = existing.version + 1
        
        self.session.add(bi_record)
        await self.session.commit()
        await self.session.refresh(bi_record)
        
        logger.info(
            "BI saved",
            extra={
                "bi_id": str(bi_record.id),
                "bi_number": bi_record.bi_number,
                "status": bi_record.status,
                "version": bi_record.version
            }
        )
        return bi_record

    async def get_by_id(self, bi_id: uuid.UUID) -> Optional[BIRecord]:
        """Recupera BI por ID."""
        result = await self.session.execute(
            select(BIRecord).where(BIRecord.id == bi_id)
        )
        return result.scalar_one_or_none()

    async def get_by_number(self, bi_number: str) -> Optional[BIRecord]:
        """Recupera BI por número."""
        result = await self.session.execute(
            select(BIRecord).where(BIRecord.bi_number == bi_number)
        )
        return result.scalar_one_or_none()

    async def get_by_citizen(self, citizen_fuc_id: str, limit: int = 50) -> List[BIRecord]:
        """Lista todos os BIs de um cidadão."""
        result = await self.session.execute(
            select(BIRecord)
            .where(BIRecord.citizen_fuc_id == citizen_fuc_id)
            .order_by(BIRecord.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_active_by_citizen(self, citizen_fuc_id: str) -> Optional[BIRecord]:
        """Retorna o BI ativo do cidadão (se houver)."""
        result = await self.session.execute(
            select(BIRecord).where(
                and_(
                    BIRecord.citizen_fuc_id == citizen_fuc_id,
                    BIRecord.status == "active"
                )
            )
        )
        return result.scalar_one_or_none()

    async def update_status(
        self, bi_id: uuid.UUID, new_status: str, reason: Optional[str] = None
    ) -> Optional[BIRecord]:
        """Atualiza status de um BI com auditoria."""
        bi_record = await self.get_by_id(bi_id)
        if not bi_record:
            return None
        
        bi_record.status = new_status
        bi_record.reason_for_status = reason
        bi_record.version += 1
        
        await self.session.commit()
        await self.session.refresh(bi_record)
        
        logger.info(
            "BI status updated",
            extra={
                "bi_id": str(bi_id),
                "new_status": new_status,
                "reason": reason,
                "version": bi_record.version
            }
        )
        return bi_record

    async def list_all(self, limit: int = 100, offset: int = 0) -> List[BIRecord]:
        """Lista BIs com paginação."""
        result = await self.session.execute(
            select(BIRecord)
            .order_by(BIRecord.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def count_by_status(self, status: str) -> int:
        """Conta BIs por status."""
        result = await self.session.execute(
            select(BIRecord).where(BIRecord.status == status)
        )
        return len(result.scalars().all())
