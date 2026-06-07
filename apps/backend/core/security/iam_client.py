"""Unified IAM Client - Single source of truth for authentication/authorization."""

from typing import Any


class IAMClient:
    """Centralized IAM client for all modules.

    Consolidates 4 duplicate implementations:
    - app/modules/bi/integrations/iam_client.py
    - app/modules/service_requests/integrations/iam_client.py
    - app/modules/statistics/integrations/iam_client.py
    - app/modules/workflow/integrations/iam_client.py
    """

    @staticmethod
    def get_current_user(token: str | None = None) -> dict[str, Any]:
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
                "bi:view",
                "bi:admin",
                "bi:export",
                "service_requests:view",
                "service_requests:manage",
                "statistics:view",
                "statistics:export",
                "workflow:view",
                "workflow:manage",
            ],
        }

    @staticmethod
    def check_permission(user: dict[str, Any] | None, perm: str) -> bool:
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
    def get_user_permissions(user: dict[str, Any] | None) -> list:
        """Get all user permissions.

        Args:
            user: User object

        Returns:
            List of permission strings
        """
        if not user:
            return []
        return user.get("permissions", [])
