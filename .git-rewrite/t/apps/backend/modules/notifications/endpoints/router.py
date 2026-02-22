from fastapi import APIRouter

router = APIRouter(
    tags=["Notifications"],
    responses={404: {"description": "Not found"}},
)
