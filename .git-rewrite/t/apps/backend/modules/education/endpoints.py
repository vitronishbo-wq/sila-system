from fastapi import APIRouter

router = APIRouter()


@router.get("/education/ping")
async def ping():
    return {"status": "ok", "module": "education"}
