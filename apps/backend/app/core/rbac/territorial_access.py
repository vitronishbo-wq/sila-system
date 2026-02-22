"""
RBAC Middleware para Controle Territorial Hierárquico

Implementa verificações de acesso baseado na hierarquia territorial:
- CENTRAL (national): acesso a tudo
- PROVINCIAL: acesso a sua província + descendentes
- MUNICIPAL: acesso a seu município + comunas
- COMMUNAL: acesso apenas a sua comuna
- CITIZEN: acesso apenas ao seu contexto pessoal
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.core.iam.models.user import User
import logging

logger = logging.getLogger(__name__)


class TerritorialAccessDenied(HTTPException):
    """Exception para acesso negado por boundary territorial"""
    def __init__(self, user_email: str, territory_id: Optional[str], detail: str = "Acesso negado por boundary territorial"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
        self.user_email = user_email
        self.territory_id = territory_id
        logger.warning(f"🚫 RBAC Territorial Denied: {user_email} tried to access territory {territory_id}")


async def verify_territorial_access(
    user: User = Depends(get_current_user),
    resource_territory_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency que verifica acesso territorial do usuário a um recurso.
    
    Regras:
    - Se resource_territory_id é None → acesso aberto (ex: login, profile)
    - Se user.territory_id é NULL → acesso NACIONAL (vê tudo) [ADMIN_CENTRAL]
    - Caso contrário → verifica se territory_id está na árvore do resource
    
    Args:
        user: Usuário autenticado (do JWT)
        resource_territory_id: ID do território do recurso (None = sem restrição)
        db: Sessão do banco
    
    Returns:
        User: Usuário se tiver permissão
        
    Raises:
        TerritorialAccessDenied: Se não tiver permissão
    """
    
    # Sem restrição territorial no recurso
    if resource_territory_id is None:
        return user
    
    # Usuário com acesso nacional (CENTRAL)
    if user.territory_id is None:
        logger.info(f"✅ {user.email} (CENTRAL) has access to all territories")
        return user
    
    # Verificar se territory_id do usuário está na árvore do resource
    # Usa closure table para hierarquias rápidas
    result = await db.execute(
        select(1).select_from(__import__('sqlalchemy').literal_column('territory_closure tc')).where(
            and_(
                __import__('sqlalchemy').literal_column('tc.ancestor_id') == str(user.territory_id),
                __import__('sqlalchemy').literal_column('tc.descendant_id') == str(resource_territory_id)
            )
        ).limit(1)
    )
    
    # Se encontrou na closure table, tem permissão
    if result.scalar() is not None:
        logger.info(f"✅ {user.email} (territory={user.territory_id}) can access resource (territory={resource_territory_id})")
        return user
    
    # Senão, foi negado
    raise TerritorialAccessDenied(
        user_email=user.email,
        territory_id=resource_territory_id,
        detail="Você não tem permissão para acessar este recurso (fora da sua jurisdição territorial)"
    )


async def verify_same_territory_or_child(
    user: User = Depends(get_current_user),
    resource_territory_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Verificação mais permissiva: permite acesso se o usuário é do mesmo nível ou superior.
    
    Usado quando um recurso não deve ser acessível por peers (ex: dados municipais não por outro munic).
    """
    
    if resource_territory_id is None:
        return user
    
    # CENTRAL sempre pode
    if user.territory_id is None:
        return user
    
    # Mesmo território
    if str(user.territory_id) == str(resource_territory_id):
        logger.info(f"✅ {user.email} accessing own territory {resource_territory_id}")
        return user
    
    # Usar closure: user.territory como ANCESTOR do resource
    result = await db.execute(
        select(1).select_from(__import__('sqlalchemy').literal_column('territory_closure tc')).where(
            and_(
                __import__('sqlalchemy').literal_column('tc.ancestor_id') == str(user.territory_id),
                __import__('sqlalchemy').literal_column('tc.descendant_id') == str(resource_territory_id),
                __import__('sqlalchemy').literal_column('tc.depth') > 0  # depth > 0 = é descendente
            )
        ).limit(1)
    )
    
    if result.scalar() is not None:
        logger.info(f"✅ {user.email} (parent of {resource_territory_id}) can access")
        return user
    
    raise TerritorialAccessDenied(
        user_email=user.email,
        territory_id=resource_territory_id,
        detail="Você não tem permissão (apenas superior hierárquico pode acessar este recurso)"
    )


# Factory para criar dependency dinâmico com territory do recurso
def require_territorial_access(resource_territory_id: Optional[str] = None):
    """
    Factory que retorna dependency com territory específico.
    
    Uso:
        @router.get("/data/{id}")
        async def get_data(id: str, user: User = Depends(require_territorial_access("territory_id"))):
            ...
    """
    async def _verify(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ) -> User:
        if resource_territory_id is None:
            return user
        
        if user.territory_id is None:
            return user
        
        from sqlalchemy import text
        
        # Query closure table
        query = """
        SELECT 1 FROM territory_closure 
        WHERE ancestor_id = %s AND descendant_id = %s
        LIMIT 1
        """
        
        result = await db.execute(
            text(query),
            {"ancestor_id": str(user.territory_id), "descendant_id": str(resource_territory_id)}
        )
        
        if result.scalar() is None:
            raise TerritorialAccessDenied(
                user_email=user.email,
                territory_id=resource_territory_id
            )
        
        return user
    
    return _verify


# Verificação por role (simpler, não usa territory)
async def require_admin(user: User = Depends(get_current_user)) -> User:
    """Apenas usuários ADMIN_CENTRAL podem"""
    if user.territory_id is not None and user.level != "national":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administrador central pode executar esta ação"
        )
    return user


async def require_not_citizen(user: User = Depends(get_current_user)) -> User:
    """Bloqueia acesso a cidadãos simples"""
    if user.role == "CITIZEN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cidadãos não podem executar esta ação"
        )
    return user
