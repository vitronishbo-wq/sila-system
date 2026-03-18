"""
Permission Guard for FastAPI Route Protection

Provides reusable FastAPI dependencies and middleware for enforcing policies.
Replaces scattered permission checks across modules.

Features:
- FastAPI Depends compatible guards
- Async-first design
- Policy evaluation integration
- Detailed access denial responses
- Audit logging hooks
"""

from typing import Callable, List, Optional, Set
from fastapi import HTTPException, Request, Depends
from functools import lru_cache

from ..policies.policy_engine import PolicyEngine, AccessDecision


class PermissionGuard:
    """
    FastAPI-integrated permission guard for route protection.
    
    Evaluates access decisions using PolicyEngine and raises
    HTTP 403 for denied access.
    
    Usage in FastAPI routes:
        from fastapi import FastAPI
        from core.auth import PermissionGuard, PolicyEngine
        
        engine = PolicyEngine()
        guard = PermissionGuard(engine)
        
        app = FastAPI()
        
        @app.get("/admin/users")
        async def list_users(
            current_user = Depends(guard.require_role("admin")),
        ):
            return {"users": []}
    """
    
    def __init__(self, policy_engine: PolicyEngine):
        """
        Initialize permission guard with policy engine.
        
        Args:
            policy_engine: PolicyEngine instance for access decisions
        """
        self.engine = policy_engine
    
    async def check_permission(
        self,
        request: Request,
        resource: str,
        action: str,
    ) -> AccessDecision:
        """
        Check if request has permission for resource action.
        
        Expects request.state.user to be a dict-like object with 'roles' key.
        Set by AuthMiddleware or similar authentication middleware.
        
        Args:
            request: FastAPI Request object
            resource: Resource being accessed
            action: Action being performed
            
        Returns:
            AccessDecision with permission result
            
        Raises:
            HTTPException: If user not authenticated or permission denied
        """
        # Extract user from request state
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )
        
        # Extract user roles
        user_roles = self._extract_roles(user)
        
        # Evaluate policy
        decision = self.engine.authorize(
            user_roles=user_roles,
            resource=resource,
            action=action,
        )
        
        if not decision.allowed:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: {decision.reason}"
            )
        
        return decision
    
    def require_role(self, *required_roles: str) -> Callable:
        """
        Create a FastAPI Depends for role-based access.
        
        Args:
            required_roles: One or more role names (user must have at least one)
            
        Returns:
            FastAPI dependency function
            
        Example:
            @app.get("/admin")
            async def admin_only(
                user = Depends(guard.require_role("admin", "super_admin")),
            ):
                pass
        """
        required_set = set(required_roles)
        
        async def dependency(request: Request) -> dict:
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Authentication required"
                )
            
            user_roles = self._extract_roles(user)
            
            if not user_roles.intersection(required_set):
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires one of: {', '.join(required_set)}"
                )
            
            return user
        
        return dependency
    
    def require_permission(
        self,
        resource: str,
        action: str,
    ) -> Callable:
        """
        Create a FastAPI Depends for policy-based access.
        
        Args:
            resource: Resource being accessed
            action: Action being performed
            
        Returns:
            FastAPI dependency function
            
        Example:
            @app.post("/documents")
            async def create_document(
                user = Depends(guard.require_permission("documents", "create")),
            ):
                pass
        """
        async def dependency(request: Request) -> dict:
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Authentication required"
                )
            
            user_roles = self._extract_roles(user)
            
            decision = self.engine.authorize(
                user_roles=user_roles,
                resource=resource,
                action=action,
            )
            
            if not decision.allowed:
                raise HTTPException(
                    status_code=403,
                    detail=decision.reason
                )
            
            return user
        
        return dependency

    def required_permission(self, permission: str) -> Callable:
        """
        Backward-compatible permission helper that accepts a single string.

        Supported formats:
        - "resource:action"
        - "resource.action"
        - "resource" (defaults to action "access")
        """
        resource, action = self._split_permission(permission)
        return self.require_permission(resource, action)
    
    def require_multiple_roles(
        self,
        roles: List[str],
        require_all: bool = False,
    ) -> Callable:
        """
        Create a FastAPI Depends for multiple role checking.
        
        Args:
            roles: List of role names to check
            require_all: If True, user must have ALL roles (AND logic).
                        If False, user must have AT LEAST ONE (OR logic).
                        
        Returns:
            FastAPI dependency function
        """
        async def dependency(request: Request) -> dict:
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Authentication required"
                )
            
            user_roles = self._extract_roles(user)
            roles_set = set(roles)
            
            if require_all:
                if not roles_set.issubset(user_roles):
                    raise HTTPException(
                        status_code=403,
                        detail=f"Requires all roles: {', '.join(roles)}"
                    )
            else:
                if not user_roles.intersection(roles_set):
                    raise HTTPException(
                        status_code=403,
                        detail=f"Requires one of: {', '.join(roles)}"
                    )
            
            return user
        
        return dependency
    
    def is_superuser(self) -> Callable:
        """
        Create a FastAPI Depends that requires a superuser role.
        
        Returns:
            FastAPI dependency function
            
        Example:
            @app.delete("/system/config")
            async def delete_config(
                user = Depends(guard.is_superuser()),
            ):
                pass
        """
        return self.require_role(*PolicyEngine.SUPERUSER_ROLES)
    
    def _extract_roles(self, user: any) -> Set[str]:
        """
        Extract roles from user object.
        
        Handles multiple user object formats:
        - dict with 'roles' key
        - object with 'roles' attribute
        
        Args:
            user: User object (dict or object instance)
            
        Returns:
            Set of role strings
        """
        if isinstance(user, dict):
            roles = user.get("roles", [])
        else:
            roles = getattr(user, "roles", [])
        
        # Normalize to set
        if isinstance(roles, set):
            return roles
        elif isinstance(roles, (list, tuple)):
            return set(roles)
        elif isinstance(roles, str):
            return {roles}
        else:
            return set()

    @staticmethod
    def _split_permission(permission: str) -> tuple[str, str]:
        if not permission:
            return ("", "access")
        if ":" in permission:
            resource, action = permission.split(":", 1)
        elif "." in permission:
            parts = permission.split(".")
            if len(parts) == 1:
                return (permission.strip(), "access")
            resource = ".".join(parts[:-1])
            action = parts[-1]
        else:
            return (permission.strip(), "access")
        resource = resource.strip()
        action = action.strip() if action else "access"
        return (resource, action)


class DynamicPermissionGuard(PermissionGuard):
    """
    Extended permission guard with attribute-based access control (ABAC).
    
    Allows checking permissions based on resource attributes and user attributes,
    not just roles.
    """
    
    def with_attribute_check(
        self,
        resource: str,
        action: str,
        check_fn: Callable[[dict, dict], bool],
    ) -> Callable:
        """
        Create a Depends that checks both role and resource attributes.
        
        Args:
            resource: Resource type
            action: Action to perform
            check_fn: Function(user_dict, request_data) -> bool for attribute checks
            
        Returns:
            FastAPI dependency function
            
        Example:
            async def check_owner(user, data):
                return user.get("id") == data.get("owner_id")
            
            @app.put("/documents/{doc_id}")
            async def update_document(
                doc_id: str,
                data: DocumentUpdate,
                user = Depends(
                    guard.with_attribute_check(
                        "documents", "update", check_owner
                    )
                ),
            ):
                pass
        """
        async def dependency(request: Request) -> dict:
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Authentication required"
                )
            
            # Check role-based permission
            user_roles = self._extract_roles(user)
            decision = self.engine.authorize(
                user_roles=user_roles,
                resource=resource,
                action=action,
            )
            
            if not decision.allowed:
                raise HTTPException(
                    status_code=403,
                    detail=decision.reason
                )
            
            # Check attribute-based permission
            try:
                user_dict = user if isinstance(user, dict) else vars(user)
                request_data = getattr(request.state, "body", {})
                
                if not check_fn(user_dict, request_data):
                    raise HTTPException(
                        status_code=403,
                        detail="Access denied: resource attribute check failed"
                    )
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Permission check failed: {str(e)}"
                )
            
            return user
        
        return dependency
