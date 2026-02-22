"""Citizenship router - minimal endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["Citizenship"])


@router.get("/ping")
async def ping():
    return {"status": "citizenship ok"}


@router.get("/requests")
async def list_requests():
    return {"requests": []}
