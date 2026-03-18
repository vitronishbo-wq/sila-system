"""
Centralized Policy Engine for Authorization

Provides the "Who can do what" policy evaluation engine.
Replaces scattered policy logic across modules.

Features:
- Role-based access policies
- Resource and action-based policies
- Dynamic policy registration
- Built-in superuser elevation
- Caching support for performance
"""

from typing import List, Set, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum


class PolicyAction(Enum):
    """Standard actions for policy evaluation"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    APPROVE = "approve"
    ADMIN = "admin"
    CREATE = "create"
    UPDATE = "update"
    EXECUTE = "execute"


@dataclass
class AccessDecision:
    """Result of policy evaluation"""
    allowed: bool
    reason: str
    policy_matched: Optional[str] = None
    
    def __bool__(self) -> bool:
        """Allow use in if statements"""
        return self.allowed


@dataclass
class ResourcePolicy:
    """Policy definition for a resource"""
    resource: str
    action: PolicyAction
    required_roles: Set[str] = field(default_factory=set)
    deny_roles: Set[str] = field(default_factory=set)
    description: str = ""
    
    def matches_action(self, action: str) -> bool:
        """Check if action matches this policy"""
        try:
            return self.action == PolicyAction(action.lower())
        except ValueError:
            return self.action.value == action.lower()


class PolicyEngine:
    """
    Centralized policy evaluation engine for SILA.
    
    Provides a single source of truth for "Who can do what".
    
    Usage:
        engine = PolicyEngine()
        engine.register_policy("users", "read", roles={"admin", "user"})
        
        # Check access
        decision = engine.authorize(
            user_roles={"user"},
            resource="users",
            action="write"
        )
        if decision:
            # Allow access
    """
    
    # Built-in superuser roles that bypass all policies
    SUPERUSER_ROLES = {"admin", "super_admin", "root", "system"}
    
    def __init__(self):
        """Initialize policy engine with empty policies"""
        self.policies: Dict[str, Dict[str, ResourcePolicy]] = {}
        self._cache: Dict[str, bool] = {}
    
    def register_policy(
        self,
        resource: str,
        action: str,
        required_roles: Optional[Set[str]] = None,
        deny_roles: Optional[Set[str]] = None,
        description: str = "",
    ) -> None:
        """
        Register an access policy for a resource action.
        
        Args:
            resource: Resource being protected (e.g., "users", "documents")
            action: Action being performed (e.g., "read", "write", "delete")
            required_roles: Set of roles that can perform this action
            deny_roles: Set of roles explicitly denied this action
            description: Human-readable policy description
        """
        if resource not in self.policies:
            self.policies[resource] = {}
        
        try:
            policy_action = PolicyAction(action.lower())
        except ValueError:
            raise ValueError(f"Unknown action: {action}. Use PolicyAction enum.")
        
        self.policies[resource][policy_action.value] = ResourcePolicy(
            resource=resource,
            action=policy_action,
            required_roles=required_roles or set(),
            deny_roles=deny_roles or set(),
            description=description,
        )
        
        # Invalidate cache when new policy registered
        self._cache.clear()
    
    def authorize(
        self,
        user_roles: Set[str],
        resource: str,
        action: str,
    ) -> AccessDecision:
        """
        Evaluate access decision for user + resource + action.
        
        Access is granted if:
        1. User has a superuser role, OR
        2. User has at least one required role AND no deny roles, OR
        3. No policy exists for resource (permissive default)
        
        Args:
            user_roles: Set of roles assigned to user
            resource: Resource being accessed
            action: Action being requested
            
        Returns:
            AccessDecision with allowed/denied status and reason
        """
        # Check cache
        cache_key = self._make_cache_key(user_roles, resource, action)
        if cache_key in self._cache:
            return AccessDecision(
                allowed=self._cache[cache_key],
                reason="Cached decision"
            )
        
        # Fast path: superuser always allowed
        if user_roles.intersection(self.SUPERUSER_ROLES):
            decision = AccessDecision(
                allowed=True,
                reason="Superuser role",
                policy_matched="SUPERUSER_ELEVATION"
            )
            self._cache[cache_key] = decision.allowed
            return decision
        
        # Check if policy exists
        if resource not in self.policies:
            decision = AccessDecision(
                allowed=True,
                reason="No policy defined (permissive default)"
            )
            self._cache[cache_key] = decision.allowed
            return decision
        
        # Check action policy
        if action.lower() not in self.policies[resource]:
            decision = AccessDecision(
                allowed=True,
                reason=f"No policy for action '{action}' (permissive default)"
            )
            self._cache[cache_key] = decision.allowed
            return decision
        
        policy = self.policies[resource][action.lower()]
        
        # Check deny list first
        if user_roles.intersection(policy.deny_roles):
            decision = AccessDecision(
                allowed=False,
                reason=f"User role in deny list for {resource}/{action}",
                policy_matched=policy.description
            )
            self._cache[cache_key] = decision.allowed
            return decision
        
        # Check required roles
        if not policy.required_roles:
            # No specific roles required
            decision = AccessDecision(
                allowed=True,
                reason=f"No roles required for {resource}/{action}",
                policy_matched=policy.description
            )
            self._cache[cache_key] = decision.allowed
            return decision
        
        # Check if user has at least one required role
        has_required_role = bool(user_roles.intersection(policy.required_roles))
        
        if has_required_role:
            decision = AccessDecision(
                allowed=True,
                reason=f"User role matches required roles for {resource}/{action}",
                policy_matched=policy.description
            )
        else:
            decision = AccessDecision(
                allowed=False,
                reason=f"User lacks required role for {resource}/{action}. "
                       f"Required: {policy.required_roles}",
                policy_matched=policy.description
            )
        
        self._cache[cache_key] = decision.allowed
        return decision
    
    def register_batch(self, policies: List[Dict[str, Any]]) -> None:
        """
        Register multiple policies at once.
        
        Args:
            policies: List of policy dictionaries with keys:
                - resource: str
                - action: str
                - required_roles: Set[str]
                - deny_roles: Optional[Set[str]]
                - description: str
        """
        for policy in policies:
            self.register_policy(
                resource=policy["resource"],
                action=policy["action"],
                required_roles=policy.get("required_roles", set()),
                deny_roles=policy.get("deny_roles", set()),
                description=policy.get("description", ""),
            )
    
    def clear_policies(self) -> None:
        """Clear all policies (use with caution)"""
        self.policies.clear()
        self._cache.clear()
    
    def get_policy(self, resource: str, action: str) -> Optional[ResourcePolicy]:
        """Get a specific policy definition"""
        if resource in self.policies:
            return self.policies[resource].get(action.lower())
        return None
    
    def list_policies(self, resource: Optional[str] = None) -> List[ResourcePolicy]:
        """
        List all registered policies.
        
        Args:
            resource: If specified, only list policies for this resource
            
        Returns:
            List of ResourcePolicy objects
        """
        if resource:
            return list(self.policies.get(resource, {}).values())
        
        all_policies = []
        for res_policies in self.policies.values():
            all_policies.extend(res_policies.values())
        return all_policies
    
    def _make_cache_key(self, roles: Set[str], resource: str, action: str) -> str:
        """Create cache key from authorization parameters"""
        roles_key = ",".join(sorted(roles))
        return f"{roles_key}:{resource}:{action.lower()}"
    
    def invalidate_cache(self) -> None:
        """Clear authorization cache (use after policy changes)"""
        self._cache.clear()
