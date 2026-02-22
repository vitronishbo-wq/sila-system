from fastapi import APIRouter

router = APIRouter(
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)
