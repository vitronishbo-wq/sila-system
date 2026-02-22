# modules/complaints/endpoints/router.py
from fastapi import APIRouter

router = APIRouter(prefix="/complaints", tags=["complaints"])