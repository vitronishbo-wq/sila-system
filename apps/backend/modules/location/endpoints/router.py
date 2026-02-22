# modules/location/endpoints/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/location", tags=["location"])