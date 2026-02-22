from fastapi import APIRouter

router = APIRouter(
    tags=["Education"],
    responses={404: {"description": "Not found"}},
)
