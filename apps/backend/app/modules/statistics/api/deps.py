from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.iam_unified import IAMClient
from ..infrastructure.repositories.statistics_repository import StatisticsRepository
from ..application.services.statistics_service import StatisticsService


def get_current_user(token: str = Depends(IAMClient.get_current_user)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


def require_permission(permission: str):
    def _dep(user=Depends(get_current_user)):
        if not IAMClient.check_permission(user, permission):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _dep


def get_statistics_repository(session: Session = Depends(get_db)) -> StatisticsRepository:
    """Dependency: Get Statistics Repository instance"""
    return StatisticsRepository(session)


def get_statistics_service(session: Session = Depends(get_db)) -> StatisticsService:
    """Dependency: Get Statistics Service instance"""
    return StatisticsService(session)
