"""Authentication utilities using JWT and SQLAlchemy."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import decode_access_token
from core.db.session import get_async_db as get_db
from core.schemas import UserRead
from modules.auth.repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_active_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_user(payload.sub)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return UserRead.model_validate(user)
