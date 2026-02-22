import logging
from fastapi import APIRouter, HTTPException, status, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import create_access_token, create_refresh_token
from config.database import get_session as get_db  # Corrigido para o padrão consolidado
from core.security import get_current_active_user
from core.scope import DataScope, get_data_scope
from modules.auth.repository import UserRepository
from modules.identity.schemas.user import UserCreate

logger = logging.getLogger(__name__)

# --- Schemas ---


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access: str
    refresh: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: Any
    email: str
    name: Optional[str] = None
    level: str
    region_id: Optional[int] = None
    is_active: bool
    created_at: Optional[Any] = None

# --- Router ---


router = APIRouter()


@router.post("/login/debug-raw")
async def debug_login_raw(request: Request):
    body = await request.body()
    headers = request.headers
    content_type = headers.get("content-type")
    print(f"--- DEBUG RAW REQUEST ---")
    print(f"Content-Type: {content_type}")
    print(f"Body: {body.decode('utf-8') if body else 'EMPTY'}")
    print(f"Headers: {headers}")
    
    # Tentativa manual de form parsing
    try:
        form = await request.form()
        print(f"Parsed Form: {form}")
    except Exception as e:
        print(f"Form Parse Error: {e}")

    return {"status": "received", "content_type": content_type, "body_size": len(body)}

@router.post("/test-form")
async def test_form(username: str = Form(...)):
    return {"message": "Form parsed successfully", "username": username}

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    OAuth2 standard login endpoint (User Specified).
    """
    user_repo = UserRepository(db)
    user = await user_repo.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token with user ID as subject
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Any = Depends(get_current_active_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.full_name,
        level=str(current_user.level),
        region_id=current_user.region_id,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    scope: DataScope = Depends(get_data_scope)
):
    user_repo = UserRepository(db)
    existing = await user_repo.get_user_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    try:
        # Criação respeitando a "cerca sanitária" do DataScope (SILA Security Pattern)
        new_user = await user_repo.create_user_scoped(payload, scope)
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.full_name,
            level=str(new_user.level),
            region_id=new_user.region_id,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    scope: DataScope = Depends(get_data_scope)
):
    user_repo = UserRepository(db)
    users = await user_repo.get_all_scoped(scope)

    return [
        UserResponse(
            id=u.id,
            email=u.email,
            name=u.full_name,
            level=str(u.level),
            region_id=u.region_id,
            is_active=u.is_active,
            created_at=u.created_at
        ) for u in users
    ]
