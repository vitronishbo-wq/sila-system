from fastapi import APIRouter

router = APIRouter()


@router.get("/registry/ping")
async def ping():
    return {"status": "ok", "module": "registry"}
