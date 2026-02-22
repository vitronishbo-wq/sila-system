# modules/registry/endpoints/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/registry", tags=["registry"])