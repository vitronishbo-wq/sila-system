"""External Connector Routes for Integration Module"""

from fastapi import APIRouter

router = APIRouter(tags=["External Connector"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "external_connector"}


# 这里可以添加外部连接器相关的路由
