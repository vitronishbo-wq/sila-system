"""Data Transformation Routes for Integration Module"""

from fastapi import APIRouter

router = APIRouter(tags=["Data Transformation"])


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": "data_transformation"}


# 这里可以添加数据转换相关的路由
