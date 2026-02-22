from fastapi import APIRouter

router = APIRouter(
    tags=["Urbanism"],
    responses={404: {"description": "Not found"}},
)
