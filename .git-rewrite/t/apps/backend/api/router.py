from fastapi import APIRouter
from fastapi import APIRouter

router = APIRouter()

# Import auth module router
from modules.auth.routes_admin import router as auth_admin_router

router.include_router(auth_admin_router, prefix="/admin", tags=["auth"])
