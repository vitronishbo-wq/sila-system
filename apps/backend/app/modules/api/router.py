from fastapi import APIRouter

router = APIRouter(tags=["api"])


@router.get("/ping")
async def ping() -> dict[str, str]:
    return {"module": "", "status": "ok"}
