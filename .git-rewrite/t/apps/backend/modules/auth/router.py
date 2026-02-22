"""
🔐 Authentication Router
Handles login, logout, token refresh, and user profile endpoints
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================
# MODELOS DE REQUEST/RESPONSE
# ============================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=3)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    roles: list[str]
    status: str
    permissions: list[str]
    created_at: Optional[str] = None


class LogoutResponse(BaseModel):
    detail: str


# ============================
# ROUTER
# ============================
router = APIRouter()


# ============================
# ENDPOINTS
# ============================
@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    """Login demo endpoint."""
    if payload.email != "admin@sila.gov.ao" or payload.password != "adm123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": "demo-access-token",
        "refresh_token": "demo-refresh-token",
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
async def get_user_profile():
    """Return demo user profile."""
    return {
        "id": "1",
        "email": "admin@sila.gov.ao",
        "name": "Administrador SILA",
        "roles": ["admin", "superuser"],
        "status": "active",
        "permissions": ["read", "write", "delete", "admin"],
        "created_at": datetime.now().isoformat(),
    }


@router.post("/logout", response_model=LogoutResponse)
async def logout():
    """Logout demo endpoint."""
    return {"detail": "Sessão terminada com sucesso"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token():
    """Refresh demo token."""
    return {
        "access_token": "demo-access-token-refreshed",
        "refresh_token": "demo-refresh-token-refreshed",
        "token_type": "bearer",
    }


@router.get("/health")
async def auth_health():
    return {"status": "healthy", "service": "auth"}
