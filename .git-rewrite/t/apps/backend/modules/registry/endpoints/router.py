from fastapi import APIRouter

router = APIRouter(
    tags=["Registry"],
    responses={404: {"description": "Not found"}},
)
