"""
Core Scope - Gerenciamento de Escopo de Dados (DPA 2024)
Implementação de Common Table Expressions (CTE) para busca recursiva de hierarquia.
"""

import logging
from typing import List, Optional, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.security import get_current_active_user
from config.database import get_session as get_db

logger = logging.getLogger(__name__)


class DataScope:
    def __init__(self, user: Any, allowed_ids: List[int]):
        """
        Controle de escopo de dados (Cerca Sanitária Digital).
        :param user: Objeto do usuário autenticado.
        :param allowed_ids: Lista de IDs geográficos permitidos (árvore recursiva).
        """
        self.user = user
        self.user_id = getattr(user, "id", None)
        # Garante que o level seja tratado como string maiúscula
        self.level = str(getattr(user, "level", "COMMUNAL")).upper()
        self.region_id = getattr(user, "region_id", None)
        self.allowed_ids = allowed_ids
        self.is_admin = (self.level == "CENTRAL" or getattr(user, "is_superuser", False))

    def apply_filter(self, query: Any, model_attr: Any) -> Any:
        """
        Aplica o filtro de escopo territorial à query SQLAlchemy.
        """
        if self.is_admin:
            return query

        # Se não houver IDs (usuário sem região), bloqueia retorno de dados por segurança
        if not self.allowed_ids:
            return query.where(text("1=0"))

        return query.where(model_attr.in_(self.allowed_ids))

    def get_filter_ids(self) -> Optional[List[int]]:
        """Retorna os IDs permitidos ou None para acesso total (Central)."""
        return None if self.is_admin else self.allowed_ids


async def get_data_scope(
    current_user: Any = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> DataScope:
    """
    Injetor de dependência que calcula a árvore de visibilidade do usuário.
    Garante que um superior veja os dados de todos os seus subordinados regionais.
    """
    user_level = str(getattr(current_user, "level", "COMMUNAL")).upper()
    user_region_id = getattr(current_user, "region_id", None)

    # Nível Central ou Superuser não precisam de filtros recursivos (vêem tudo)
    if user_level == "CENTRAL" or getattr(current_user, "is_superuser", False) or user_region_id is None:
        return DataScope(current_user, [])

    try:
        # Query Recursiva: Busca o ID da região do usuário e todos os seus descendentes na DPA
        # A tabela 'locations' foi definida na migração 001.
        recursive_query = text("""
            WITH RECURSIVE dpa_tree AS (
                -- Caso base: a região do próprio usuário
                SELECT id FROM locations WHERE id = :rid
                UNION ALL
                -- Passo recursivo: todos os descendentes (municípios -> comunas -> locais)
                SELECT l.id FROM locations l
                INNER JOIN dpa_tree dt ON l.parent_id = dt.id
            )
            SELECT id FROM dpa_tree;
        """)

        result = await db.execute(recursive_query, {"rid": user_region_id})
        # Coleta todos os IDs da árvore
        allowed_ids = list(result.scalars().all())

        return DataScope(current_user, allowed_ids)

    except Exception as e:
        logger.error(
            f"Erro ao calcular escopo recursivo para usuário {getattr(current_user, 'id', 'unknown')}: {e}")
        # Fallback de segurança: limita apenas à região imediata do usuário em caso de erro na query
        return DataScope(current_user, [user_region_id] if user_region_id else [])
