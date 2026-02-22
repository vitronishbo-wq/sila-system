from fastapi import APIRouter

router = APIRouter(
    tags=["Justice"],
    responses={404: {"description": "Not found"}},
)
