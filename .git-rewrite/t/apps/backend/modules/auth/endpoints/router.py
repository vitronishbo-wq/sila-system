"""Auth router - API endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import create_access_token, create_refresh_token
from core.db.session import get_async_db as get_db
from core.security import get_current_active_user
from modules.auth.repository import UserRepository
from modules.auth.models.user import User, UserRead
from modules.common.utils.utils import verify_password


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
router = APIRouter(tags=["Auth"])


# ============================
# ENDPOINTS
# ============================
@router.post("/test")
async def test_endpoint():
    """Endpoint de teste para verificar CORS."""
    return {"status": "ok", "message": "CORS funcionando!"}


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Login endpoint - Autenticação real com JWT.
    
    Valida credenciais contra o banco de dados e gera tokens JWT válidos.
    """
    try:
        user_repo = UserRepository(db)
        user = await user_repo.get_user_by_email(payload.email)
        
        # Validar usuário existe e está ativo
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas ou usuário inativo",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Validar senha
        if not verify_password(payload.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Gerar tokens JWT válidos
        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except HTTPException:
        raise
    except Exception as e:
        # Log do erro para debugging
        import traceback
        print(f"❌ Erro no login: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
async def get_user_profile():
    """Return user profile - Placeholder que retorna dados do admin."""
    # TODO: Integrar com get_current_active_user quando auth estiver completo
    return {
        "id": "d08699b5-f9ca-4d32-8abc-699dfaffdc8b",
        "email": "admin@sila.gov.ao",
        "name": "Administrador SILA",
        "roles": ["admin", "superuser"],
        "status": "active",
        "permissions": ["read", "write", "delete", "admin"],
        "created_at": datetime.now().isoformat(),
    }


@router.post("/logout", response_model=LogoutResponse)
async def logout():
    """Logout endpoint."""
    return {"detail": "Sessão terminada com sucesso"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token_endpoint(
    current_user = None  # Seria preenchido com token válido
):
    """
    Refresh token endpoint.
    Regenera um novo access_token usando um refresh_token válido.
    """
    # Placeholder simples para agora
    return {
        "access_token": "demo-access-token-refreshed",
        "refresh_token": "demo-refresh-token-refreshed",
        "token_type": "bearer",
    }


@router.get("/ping")
async def ping():
    """Health check."""
    return {"status": "auth ok"}


@router.get("/health")
async def auth_health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "auth"}
