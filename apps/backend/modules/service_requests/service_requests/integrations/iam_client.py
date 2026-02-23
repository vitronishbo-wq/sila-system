"""IAM client for user and permission integration"""
from typing import Optional, List, Dict, Any
from uuid import UUID


class IAMClient:
    """IAM client for authentication and authorization"""

    async def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user from token"""
        # In production, validate token with IAM module
        # For now, return mock
        return {
            "user_id": UUID(int=0),
            "email": "user@example.com",
            "roles": ["CITIZEN"],
        }

    async def get_user_roles(self, user_id: UUID) -> List[str]:
        """Get user roles"""
        # Query IAM module for user roles
        return ["CITIZEN"]

    async def check_permission(self, user_id: UUID, permission: str) -> bool:
        """Check if user has permission"""
        # Query IAM module for permissions
        # permission format: "resource:action"
        return True

    async def get_user_info(self, user_id: UUID) -> Optional[Dict[str, Any]]:
        """Get user information"""
        return {
            "user_id": str(user_id),
            "email": "user@example.com",
            "name": "User Name",
        }
