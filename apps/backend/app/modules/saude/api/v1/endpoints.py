from fastapi import APIRouter

router = APIRouter(tags=["Saude"])


@router.get("/status")
def status() -> dict:
    return {"status": "ok"}
