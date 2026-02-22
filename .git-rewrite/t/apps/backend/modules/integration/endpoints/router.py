from fastapi import APIRouter

router = APIRouter(
    tags=["Integration"],
    responses={404: {"description": "Not found"}},
)
