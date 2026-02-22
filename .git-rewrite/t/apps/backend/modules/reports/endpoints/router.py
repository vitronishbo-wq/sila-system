from fastapi import APIRouter

router = APIRouter(
    tags=["Reports"],
    responses={404: {"description": "Not found"}},
)
