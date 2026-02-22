# modules/appointments/endpoints/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/appointments", tags=["appointments"])