from fastapi import Depends, HTTPException, status, Request
from typing import Optional, List
from uuid import UUID

from .rate_limiter import RateLimiter


def get_rate_limiter() -> RateLimiter:
    """Dependency para rate limiter"""
    return RateLimiter()


def require_taxpayer_permission(permission: str):
    """Dependency para verificar permissão"""
    async def dependency(request: Request):
        user = getattr(request.state, "user", None)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não autenticado"
            )
        
        if user.get("is_superuser"):
            return True
        
        permissions = user.get("permissions", [])
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão necessária: {permission}"
            )
        return True
    return dependency


def can_access_taxpayer(taxpayer_id: UUID):
    """Dependency para verificar acesso a contribuinte"""
    async def dependency(request: Request):
        user = getattr(request.state, "user", None)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Não autenticado"
            )
        
        if user.get("is_superuser"):
            return taxpayer_id
        
        if "operator" in user.get("roles", []):
            return taxpayer_id
        
        citizen_id = user.get("citizen_id")
        if citizen_id and str(citizen_id) == str(taxpayer_id):
            return taxpayer_id
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado a este contribuinte"
        )
    return dependency


def get_current_user(request: Request):
    """Obtém usuário atual da requisição"""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    return user


def get_current_user_optional(request: Request):
    """Obtém usuário atual (opcional)"""
    return getattr(request.state, "user", None)
