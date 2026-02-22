# modules/commercial/endpoints/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/commercial", tags=["commercial"])