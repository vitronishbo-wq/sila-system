from fastapi import APIRouter

router = APIRouter(
    tags=["Governance"],
    responses={404: {"description": "Not found"}},
)

# Add your endpoints here
