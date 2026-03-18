"""Health check endpoint for module"""
from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any
router = APIRouter(tags=['health'])

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    module: str
    version: str = '1.0.0'
    details: Dict[str, Any] = {}

@router.get('/health', response_model=HealthResponse, status_code=status.HTTP_200_OK, summary='Health Check', description='Check module health status')
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Module health status
    """
    return HealthResponse(status='healthy', module=__name__.split('.')[3], details={'uptime_seconds': 0})

@router.get('/health/ready', status_code=status.HTTP_200_OK)
async def readiness_check():
    """Readiness probe for k8s"""
    return {'ready': True}

@router.get('/health/live', status_code=status.HTTP_200_OK)
async def liveness_check():
    """Liveness probe for k8s"""
    return {'alive': True}