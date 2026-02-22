from fastapi import APIRouter

router = APIRouter(
    tags=["Appointments"],
    responses={404: {"description": "Not found"}},
)
