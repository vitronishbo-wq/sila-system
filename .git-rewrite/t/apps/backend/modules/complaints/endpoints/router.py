from fastapi import APIRouter

router = APIRouter(
    tags=["Complaints"],
    responses={404: {"description": "Not found"}},
)
