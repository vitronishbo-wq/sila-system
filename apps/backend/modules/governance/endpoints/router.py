# modules/governance/endpoints/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/governance", tags=["governance"])