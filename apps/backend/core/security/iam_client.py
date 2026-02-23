"""Unified IAM Client - Single source of truth for authentication/authorization."""

from typing import Optional, Dict, Any


class IAMClient:
    """Centralized IAM client for all modules.
    
    Consolidates 4 duplicate implementations:
    - app/modules/bi/integrations/iam_client.py
    - app/modules/service_requests/integrations/iam_client.py
    - app/modules/statistics/integrations/iam_client.py
    - app/modules/workflow/integrations/iam_client.py
    """

    @staticmethod
    def get_current_user(token: Optional[str] = None) -> Dict[str, Any]:
        """Get current user from token.
        
        Args:
            token: JWT or Bearer token
            
        Returns:
            User object with id, username, permissions
        """
        # TODO: Implement real token validation with core.security
        return {
            "id": 1,
            "username": "dev",
            "permissions": [
                "bi:view", "bi:admin", "bi:export",
                "service_requests:view", "service_requests:manage",
                "statistics:view", "statistics:export",
                "workflow:view", "workflow:manage"
            ]
        }

    @staticmethod
    def check_permission(user: Optional[Dict[str, Any]], perm: str) -> bool:
        """Check if user has permission.
        
        Args:
            user: User object
            perm: Permission string
            
        Returns:
            True if user has permission
        """
        if not user:
            return False
        return perm in user.get("permissions", [])

    @staticmethod
    def get_user_permissions(user: Optional[Dict[str, Any]]) -> list:
        """Get all user permissions.
        
        Args:
            user: User object
            
        Returns:
            List of permission strings
        """
        if not user:
            return []
        return user.get("permissions", [])
