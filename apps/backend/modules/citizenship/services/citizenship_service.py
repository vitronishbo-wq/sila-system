import logging
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..models.atualizacao_bi import AtualizacaoBI, AtualizacaoBIDocument

logger = logging.getLogger(__name__)

class CitizenshipService:
    """Classe para operações de cidadania usando padrão Async 2.0."""

    @staticmethod
    async def get_user_updates(db: AsyncSession, user_id: int) -> List[AtualizacaoBI]:
        """Busca todos os pedidos de atualização de BI de um usuário."""
        try:
            result = await db.execute(
                select(AtualizacaoBI)
                .where(AtualizacaoBI.user_id == user_id)
                .order_by(AtualizacaoBI.data_criacao.desc())
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Erro ao buscar atualizações do usuário {user_id}: {e}")
            raise

    @staticmethod
    async def get_update_by_id(db: AsyncSession, update_id: int) -> Optional[AtualizacaoBI]:
        """Busca um pedido específico com todos os seus documentos anexados."""
        try:
            result = await db.execute(
                select(AtualizacaoBI)
                .options(selectinload(AtualizacaoBI.documents))
                .where(AtualizacaoBI.id == update_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Erro ao buscar pedido {update_id}: {e}")
            raise

    @staticmethod
    async def list_all_requests(db: AsyncSession) -> List[AtualizacaoBI]:
        """Lista todos os pedidos do sistema (visão administrativa)."""
        try:
            result = await db.execute(
                select(AtualizacaoBI).order_by(AtualizacaoBI.data_criacao.desc())
            )
            return list(result.scalars().all())
        except Exception as e:
            logger.error(f"Erro ao listar todos os pedidos: {e}")
            raise