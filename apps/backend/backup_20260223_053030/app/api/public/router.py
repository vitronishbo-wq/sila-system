from fastapi import APIRouter
from app.api.public.auth.routes import router as auth_router
from app.api.public.auth.citizen_routes import router as citizen_auth_router
from app.api.public.health.routes import router as health_router

public_router = APIRouter()
public_router.include_router(health_router)
public_router.include_router(auth_router)
public_router.include_router(citizen_auth_router)
