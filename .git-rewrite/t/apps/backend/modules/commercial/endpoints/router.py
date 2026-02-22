from fastapi import APIRouter

router = APIRouter(
    tags=["Commercial"],
    responses={404: {"description": "Not found"}},
)
