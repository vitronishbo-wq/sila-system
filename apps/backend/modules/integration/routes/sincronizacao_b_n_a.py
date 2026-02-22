"""BNA Synchronization Routes for Integration Module"""

from fastapi import APIRouter

router = APIRouter(tags=["BNA Synchronization"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "bna_synchronization"}


# 这里可以添加BNA同步相关的路由
