# backend/modules/auth/endpoints.py
# -*- coding: utf-8 -*-

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from core.auth import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from core.db.session import get_async_db as get_db, get_db
from core.schemas import (
    RefreshTokenRequest,
    RefreshTokenResponse,
    Token,
    UserCreate,
    UserRead,
)
from modules.auth.auth_utils import get_current_active_user
from modules.auth.repository import UserRepository

router = APIRouter()

# ✅ FASE 1: REMOVER fallback admin completamente
# Apenas autenticação real via banco de dados
# (Ambiguidade #4 resolvida - sem bypass de segurança)


@router.get("/ping")
async def ping():
    """Healthcheck—usado pelo React e monitoramento."""
    return {"status": "ok", "module": "auth"}


# -------------------------------------------------------------------------
# LOGIN MULTIFORMATO (JSON, FORM ou QUERY)
# -------------------------------------------------------------------------
@router.post("/login")
async def login(
    request: Request,
    email: Optional[str] = None,
    password: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    ✅ Login que aceita:
    - JSON (frontend React / axios)
    - FormData / x-www-form-urlencoded (HTML forms)
    - Query parameters (testes manuais)
    """

    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        data = await request.json()
        email = email or data.get("email")
        password = password or data.get("password")

    elif "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        email = email or form.get("email")
        password = password or form.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    repo = UserRepository(db)
    user = await repo.authenticate(email, password)

    if not user:
        # ✅ FASE 1: Sem fallback - apenas autenticação real
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Geração de tokens JWT
    access = create_access_token(subject=str(user.id))
    refresh = create_refresh_token(subject=str(user.id))
    user_dto = UserRead.model_validate(user)

    # ✅ FASE 1: Resposta padronizada e unificada
    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": {
            "id": str(user_dto.id),
            "email": user_dto.email,
            "is_superuser": user_dto.is_superuser,
            "roles": ["admin"] if user_dto.is_superuser else ["user"],
        },
    }


# ✅ FASE 1: REMOVER endpoint duplicado /login/access-token
# Manter apenas /login como endpoint único (Ambiguidade #3 resolvida)
#
# Se precisar compatibilidade OAuth2, adicionar suporte na rota /login


# -------------------------------------------------------------------------
# REFRESH TOKEN
# -------------------------------------------------------------------------
@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(refresh_request: RefreshTokenRequest) -> Any:

    payload = decode_refresh_token(refresh_request.refresh_token)

    new_access = create_access_token(subject=payload.sub)

    return RefreshTokenResponse(access_token=new_access)


# -------------------------------------------------------------------------
# LOGOUT
# -------------------------------------------------------------------------
@router.post("/logout")
async def logout():
    """
    Logout stateless — apenas o frontend apaga o token.
    """
    return {"message": "Logged out"}


# -------------------------------------------------------------------------
# REGISTRO DE USUÁRIO
# -------------------------------------------------------------------------
@router.post("/register", response_model=UserRead)
async def register_user(
    user_create: UserCreate, db: AsyncSession = Depends(get_db)
) -> Any:

    repo = UserRepository(db)

    existing = await repo.get_user_by_email(user_create.email)
    if existing:
        raise HTTPException(400, detail="Email already registered")

    user = await repo.create_user(user_create)
    return UserRead.model_validate(user)


# -------------------------------------------------------------------------
# TESTE TOKEN (útil para debug)
# -------------------------------------------------------------------------
@router.post("/test-token", response_model=UserRead)
async def test_token(current_user: UserRead = Depends(get_current_active_user)):
    return current_user
