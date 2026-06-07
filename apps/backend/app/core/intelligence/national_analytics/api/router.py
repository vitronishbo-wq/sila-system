from fastapi import APIRouter

from ..application.analytics_engine import NationalAnalytics

router = APIRouter(prefix="/intelligence/analytics", tags=["analytics"])
analytics = NationalAnalytics()


@router.post("/compute")
def compute(data: dict):
    """Compute national analytics aggregation"""
    result = analytics.aggregate(data)
    return result
