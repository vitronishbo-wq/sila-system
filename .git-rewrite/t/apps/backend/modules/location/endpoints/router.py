from fastapi import APIRouter

router = APIRouter(
    tags=["Location"],
    responses={404: {"description": "Not found"}},
)
