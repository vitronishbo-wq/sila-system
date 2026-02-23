from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.api.public.auth.schemas import UserRegister
from modules.identity.models.user import User
from app.core.constants import UserRole, AdminLevel
from app.core.security import verify_password, create_access_token, get_password_hash
import uuid

router = APIRouter(prefix="/auth", tags=["Auth"])

login_attempts = {}

def check_rate_limit(email: str, max_attempts: int = 5, window_seconds: int = 60):
    now = datetime.now()
    key = f"login:{email}"
    if key not in login_attempts:
        login_attempts[key] = []
    login_attempts[key] = [ts for ts in login_attempts[key] if now - ts < timedelta(seconds=window_seconds)]
    if len(login_attempts[key]) >= max_attempts:
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again later.")
    login_attempts[key].append(now)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    check_rate_limit(form_data.username)
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 🔐 Fase 1: Incluir role, level e territory_id no token
    access_token = create_access_token({
        "sub": user.email,
        "user_id": str(user.id),
        "role": user.role if isinstance(user.role, str) else user.role.value,
        "level": user.level if isinstance(user.level, str) else user.level.value,
        "territory_id": str(user.territory_id) if user.territory_id else None
    })
    
    dashboard = get_dashboard_for_role(user.role)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "level": user.level,
            "territory_id": str(user.territory_id) if user.territory_id else None,
            "citizen_id": str(user.citizen_id) if user.citizen_id else None
        },
        "navigation": {
            "dashboard": dashboard,
            "should_redirect": True,
            "redirect_to": dashboard
        },
        "message": f"Bem-vindo! A redirecionar para o seu dashboard."
    }

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role,
        "level": current_user.level,
        "operational_level": current_user.level,
        "territory_id": str(current_user.territory_id) if current_user.territory_id else None,
        "is_active": current_user.is_active,
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}

@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_user)):
    # 🔐 Fase 1: Incluir role e level no token renovado
    new_token = create_access_token({
        "sub": current_user.email,
        "role": current_user.role.value if hasattr(current_user.role, 'value') else current_user.role,
        "level": current_user.level.value if hasattr(current_user.level, 'value') else current_user.level,
    })
    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    """
    Registo inicial de cidadão.
    Cria utilizador com role CITIZEN.
    """
    # 1. Validar duplicados (Email ou NIF/Username)
    # Assumimos que o NIF será usado como username para cidadãos
    query = select(User).where(
        or_(
            User.email == user_in.email,
            User.username == user_in.nif
        )
    )
    result = await db.execute(query)
    existing_user = result.scalars().first()
    
    if existing_user:
        if existing_user.email == user_in.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="NIF already registered"
            )

    # 2. Criar FUC e Utilizador no mesmo transaction
    hashed_password = get_password_hash(user_in.password)
    citizen_uuid = uuid.uuid4()
    
    # A. Criar a Projeção FUC
    new_fuc = CitizenFUC(
        citizen_id=citizen_uuid,
        full_name=user_in.name,
        nif=user_in.nif,
        birth_date=datetime.utcnow().date(), # Placeholder, devia vir de BI futuramente
        gender="U", # Unknown/Placeholder
        vital_status=VitalStatus.ALIVE,
        last_event_id=uuid.uuid4(),
        last_updated=datetime.utcnow(),
        version=1,
        history=[]
    )
    
    # B. Criar o User vinculado à FUC
    new_user = User(
        email=user_in.email,
        username=user_in.nif,  # Mapping NIF to username
        password_hash=hashed_password,
        role=UserRole.CITIZEN,
        level=AdminLevel.CITIZEN,
        is_active=True,
        citizen_id=citizen_uuid  # ✅ Vinculo Obrigatório
    )
    
    db.add(new_fuc)
    db.add(new_user)
    
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user and FUC: {str(e)}"
        )
        
    # Generate token immediately for the response if needed, 
    # but for now we follow the user's requested structure.
    
    return {
        "message": "User created successfully", 
        "id": str(new_user.id),
        "user": {
            "id": str(new_user.id),
            "email": new_user.email,
            "role": new_user.role,
            "citizen_id": str(citizen_uuid) if citizen_uuid else None,
            "dashboard_url": get_dashboard_for_role(new_user.role)
        }
    }

def get_dashboard_for_role(role: str) -> str:
    """Retorna URL do dashboard para o papel"""
    dashboards = {
        "citizen": "/citizen/portal",
        "commune_officer": "/admin/dashboard/commune",
        "commune_admin": "/admin/dashboard/commune",
        "municipality_admin": "/admin/dashboard/municipality",
        "province_admin": "/admin/dashboard/province",
        "central_admin": "/admin/dashboard/central",
        "admin_central": "/admin/dashboard/central"
    }
    return dashboards.get(role, "/login")
