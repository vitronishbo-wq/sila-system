from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from .auth import create_access_token, create_refresh_token, verify_token
from .models import TokenResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/demo-auth/login")

# Simple in-memory user check for demo — replace with real repo in production
DEMO_USER = {"username": "admin", "password": "adm123"}


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != DEMO_USER["username"]
        or form_data.password != DEMO_USER["password"]
    ):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    access_token = create_access_token({"sub": form_data.username})
    refresh_token = create_refresh_token({"sub": form_data.username})

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh(refresh_token: Dict[str, str]):
    # Expect JSON body: {"refresh_token": "..."}
    token = refresh_token.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail="refresh_token is required")

    payload = verify_token(token)
    new_access = create_access_token({"sub": payload.get("sub")})
    return {"access_token": new_access}


@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return {"message": f"Acesso permitido para {payload.get('sub')}"}
