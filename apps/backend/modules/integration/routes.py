"""Integration Module Routes"""

from fastapi import APIRouter

router = APIRouter(tags=["Integration"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "module": "integration"}


# 这里可以添加更多集成模块的路由
