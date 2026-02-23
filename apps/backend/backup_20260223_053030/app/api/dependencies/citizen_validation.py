"""
Middleware dependencies for citizen validation.

This module provides reusable dependency functions for extracting and validating
citizen IDs from authenticated requests, eliminating duplicated validation logic
across endpoints.
"""

from typing import Any, Dict
from uuid import UUID
from fastapi import HTTPException, Depends

from app.api.deps import get_current_user, get_current_citizen
from modules.identity.models.user import User


async def extract_citizen_id(
    current_user: User = Depends(get_current_user)
) -> UUID:
    """
    Extract and validate citizen_id from current user.
    
    Converts string citizen_id to UUID and ensures it exists.
    This is a reusable dependency to eliminate duplicated validation logic
    across multiple endpoints.
    
    Args:
        current_user: Current authenticated user (from get_current_user)
    
    Returns:
        UUID: The validated citizen ID
    
    Raises:
        HTTPException: 400 if citizen_id not found in current_user
        HTTPException: 400 if citizen_id cannot be converted to UUID
    """
    citizen_id = current_user.citizen_id
    if not citizen_id:
        raise HTTPException(
            status_code=400,
            detail="Cidadão não identificado"
        )
    
    try:
        # Handle both string and UUID inputs
        if isinstance(citizen_id, UUID):
            return citizen_id
        return UUID(str(citizen_id))
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"ID de cidadão inválido: {str(e)}"
        )


async def extract_citizen_id_from_token(
    current_user: User = Depends(get_current_user)
) -> str:
    """
    Extract citizen_id as string from current user (alternative for backward compatibility).
    
    Args:
        current_user: Current authenticated user (from get_current_user)
    
    Returns:
        str: The citizen ID as string
    
    Raises:
        HTTPException: 401 if citizen_id not found
    """
    citizen_id = current_user.citizen_id
    if not citizen_id:
        raise HTTPException(
            status_code=401,
            detail="Cidadão não autenticado"
        )
    return str(citizen_id)


async def extract_citizen_id_from_current(
    current_citizen: Dict[str, Any] = Depends(get_current_citizen)
) -> UUID:
    """
    Extract and validate citizen_id from current_citizen (enriched user with FUC data).
    
    This is for endpoints that use get_current_citizen dependency,
    which already validates the citizen exists in FUC system.
    
    Args:
        current_citizen: Current authenticated citizen with FUC data (from get_current_citizen)
    
    Returns:
        UUID: The validated citizen ID
    
    Raises:
        HTTPException: 401 if citizen_id not found or invalid
    """
    citizen_id = current_citizen.get("citizen_id")
    if not citizen_id:
        raise HTTPException(
            status_code=401,
            detail="Cidadão não autenticado"
        )
    
    try:
        # Handle both string and UUID inputs
        if isinstance(citizen_id, UUID):
            return citizen_id
        return UUID(citizen_id)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=401,
            detail=f"ID de cidadão inválido: {str(e)}"
        )

