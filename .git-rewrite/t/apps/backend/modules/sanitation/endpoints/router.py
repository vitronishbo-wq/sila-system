from fastapi import APIRouter

router = APIRouter(
    tags=["Sanitation"],
    responses={404: {"description": "Not found"}},
)
