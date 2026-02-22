"""
Core security utilities and dependency injection functions (FastAPI Dependencies).
Provides password hashing, token creation, and dummy user dependencies until the full Auth module is registered.
"""

from datetime import datetime, timedelta
from typing import Annotated, Optional, Dict

from fastapi import Depends, HTTPException, Request, status
from jose import jwt
from passlib.context import CryptContext

# Importar configurações
from config.settings import settings

# ⚠️ CRÍTICO: AUTH_SECRET_KEY deve estar em settings via .env
# Se não estiver configurado, lançar erro em tempo de inicialização
if not settings.AUTH_SECRET_KEY or settings.AUTH_SECRET_KEY == "change_me_immediately":
    raise ValueError(
        "❌ AUTH_SECRET_KEY não configurado! Defina AUTH_SECRET_KEY em .env ou .env.development"
    )

SECRET_KEY = settings.AUTH_SECRET_KEY
ALGORITHM = getattr(settings, "ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 30)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔑 Funções de senha
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 🔑 Função para criar token JWT
def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 🧑 Dependências de usuário (mock)
async def get_current_user(request: Request) -> Dict:
    """
    Retorna um usuário fictício para testes.
    Em produção, validar JWT e buscar no banco.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        # Mock user
        return {"id": 1, "username": "testuser"}
    # TODO: validar token
    return {"id": 1, "username": "testuser"}


async def get_current_active_user(request: Request) -> Dict:
    """
    Retorna um usuário ativo fictício para testes.
    """
    user = await get_current_user(request)
    if not user.get("active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return {**user, "active": True}


# Dependency annotation para endpoints FastAPI
CurrentUser = Annotated[Dict, Depends(get_current_user)]
