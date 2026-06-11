"""Security core module - Centralized authentication and authorization."""

import logging
from typing import Optional

import bcrypt
from apps.backend.config.database import get_db
from apps.backend.core.auth import JWTHandler
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .iam_client import IAMClient

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)
security_dep = Depends(security)
db_dep = Depends(get_db)


def get_password_hash(password: str) -> str:
    """Hash password using bcrypt."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception as e:
        logger.error(f"Erro na verificação de senha: {e}")
        return False


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = security_dep,
    db: AsyncSession = db_dep,
):
    """Get current authenticated user."""
    from apps.backend.config.settings import settings

    from apps.backend.app.modules.identity.models.user import User

    token = None
    if credentials:
        token = credentials.credentials
    else:
        token = request.query_params.get("token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não fornecido ou inválido"
        )

    try:
        jwt_handler = JWTHandler(secret_key=settings.SECRET_KEY)
        payload = jwt_handler.decode_token(token)
        username = payload.get("sub")
        if not username:
            raise ValueError("Token inválido")
    except Exception as e:
        logger.warning(f"Erro de decodificação de token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado"
        ) from e

    result = await db.execute(select(User).where(User.email == username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado"
        )

    return user


current_user_dep = Depends(get_current_user)


async def get_current_active_user(current_user=current_user_dep):
    """Get current active user (must be active)."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")
    return current_user


current_active_user_dep = Depends(get_current_active_user)


async def get_current_superuser(current_user=current_active_user_dep):
    """Get current superuser (must have admin role)."""
    roles = getattr(current_user, "roles", [])
    if "admin" not in roles and not getattr(current_user, "is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores"
        )
    return current_user


__all__ = [
    "IAMClient",
    "get_current_user",
    "get_current_active_user",
    "get_current_superuser",
    "get_password_hash",
    "verify_password",
]
