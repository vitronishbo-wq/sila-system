import uuid
from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_session
from modules.identity.models.user import User
from app.core.constants import UserRole
from app.core.settings import settings
from app.core.security import ALGORITHM
from app.core.helpers import safe_get
from app.core.notifications.services.notification_service import NotificationService

# Alias for consistency - get_db is commonly used name for database dependencies
get_db = get_session

# Backwards-compatible alias: some modules import 
get_db_async = get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.email == user_email))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user


# ============================================================================
# 🔐 ROLE-BASED GUARDS (Fase 1: Segurança de Identidade)
# ============================================================================

async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Guard para endpoints administrativos.
    Valida que o user é admin (qualquer nível de administração).
    
    Usado em: /admin/* endpoints
    Levanta: 403 Forbidden se o user for cidadão
    """
    ADMIN_ROLES = {
        UserRole.ADMIN_SUPER,
        UserRole.ADMIN_CENTRAL,
        UserRole.ADMIN_PROVINCIAL,
        UserRole.ADMIN_MUNICIPAL,
        UserRole.ADMIN_COMMUNAL,
    }

    if current_user.role not in ADMIN_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso administrativo requerido. Apenas administradores são autorizados.",
        )

    return current_user


async def get_current_citizen_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Guard para endpoints do cidadão.
    Valida que o user é um cidadão (role=CITIZEN).
    
    Usado em: /citizen/* endpoints
    Levanta: 403 Forbidden se o user for admin
    """
    if current_user.role != UserRole.CITIZEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso exclusivo para cidadãos. Apenas utilizadores com role CITIZEN são autorizados.",
        )

    return current_user

async def get_current_citizen(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Dependência específica para cidadãos.
    Retorna dicionário com dados do User + dados do CitizenFUC.
    """
    if current_user.role != UserRole.CITIZEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a cidadãos"
        )
    
    if not current_user.citizen_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cidadão não possui perfil FUC associado"
        )
    
    from app.citizen.core.models import CitizenFUC
    result = await db.execute(
        select(CitizenFUC).where(CitizenFUC.citizen_id == current_user.citizen_id)
    )
    citizen = result.scalar_one_or_none()
    
    if not citizen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registo FUC não encontrado para este cidadão"
        )
    
    return {
        "user_id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
        "citizen_id": str(citizen.citizen_id),
        "full_name": safe_get(citizen, "full_name"),
        "province_id": safe_get(citizen, "province_id"),
        "municipality_id": safe_get(citizen, "municipality_id"),
        "commune_id": safe_get(citizen, "commune_id"),
        "email_citizen": safe_get(citizen, "email"),
        "phone": safe_get(citizen, "phone")
    }


async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Dependência para administradores (Central, Provincial, Municipal, Comunal).
    Retorna o user model como dicionário para compatibilidade.
    """
    admin_roles = {
        UserRole.ADMIN_SUPER,
        UserRole.ADMIN_CENTRAL,
        UserRole.ADMIN_PROVINCIAL,
        UserRole.ADMIN_MUNICIPAL,
        UserRole.ADMIN_COMMUNAL,
    }
    
    if current_user.role not in admin_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )
    
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
        "territory_id": current_user.territory_id
    }

async def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    """Injeta a instância do serviço de notificações."""
    return NotificationService(db)
