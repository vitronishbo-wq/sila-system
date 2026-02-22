from fastapi import APIRouter, HTTPException, status, Depends, Form
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from jwt.exceptions import InvalidTokenError

from core.auth import create_access_token, create_refresh_token, decode_refresh_token
from config.database import get_db
from core.security import get_current_active_user, verify_password
from modules.identity.models.user import User
from sqlalchemy import select

router = APIRouter(tags=["Auth"])

# --- Esquemas de Dados ---

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    bi_number: Optional[str] = None
    is_active: bool
    is_verified: bool
    status: str
    administrative_level: str
    region_id: Optional[int] = None
    roles: List[str]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LogoutResponse(BaseModel):
    detail: str

# --- Endpoints ---

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador inativo ou não encontrado",
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )
    
    access_token = create_access_token(subject=user.email)
    refresh_token = create_refresh_token(subject=user.email)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.post("/logout", response_model=LogoutResponse)
async def logout():
    return {"detail": "Sessão terminada com sucesso"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Form(..., description="Refresh token obtido no login"),
    db: AsyncSession = Depends(get_db)
):
    """
    Renova o access token usando um refresh token válido.
    """
    try:
        decoded = decode_refresh_token(refresh_token)
        user_email = decoded.sub
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Refresh token inválido ou expirado: {str(e)}",
        )
    
    # Verificar se o utilizador ainda existe e está ativo
    result = await db.execute(select(User).where(User.email == user_email))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilizador não encontrado ou inativo",
        )
    
    # Gerar novos tokens
    new_access_token = create_access_token(subject=user.email)
    new_refresh_token = create_refresh_token(subject=user.email)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
