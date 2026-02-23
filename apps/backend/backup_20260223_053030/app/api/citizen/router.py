from fastapi import APIRouter
from app.api.citizen.requests import router as requests_router

citizen_router = APIRouter()
citizen_router.include_router(requests_router)
