"""API Gateway Routes for Integration Module"""

from fastapi import APIRouter

router = APIRouter(tags=["API Gateway"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "api_gateway"}


# 这里可以添加API网关相关的路由
