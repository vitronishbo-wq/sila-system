"""
Centralized Role Management System

Defines role hierarchy, inheritance, and permissions.
Single source of truth for role definitions across SILA.

Features:
- Role hierarchy and inheritance
- Permission aggregation through hierarchy
- Role-to-policy mapping
- Role metadata and descriptions
"""

from dataclasses import dataclass, field
from enum import Enum


class SystemRole(Enum):
    """Built-in system roles"""

    ROOT = "root"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"
    SERVICE = "service"
    SYSTEM = "system"


@dataclass
class RoleDefinition:
    """Definition of a role with hierarchy and metadata"""

    name: str
    description: str = ""
    parent_roles: set[str] = field(default_factory=set)
    permissions: set[str] = field(default_factory=set)
    metadata: dict[str, any] = field(default_factory=dict)

    def get_all_permissions(self, manager: "RoleManager") -> set[str]:
        """
        Get all permissions including inherited from parent roles.

        Args:
            manager: RoleManager instance for hierarchy lookup

        Returns:
            Set of all permissions (direct + inherited)
        """
        all_perms = self.permissions.copy()
        for parent in self.parent_roles:
            all_perms.update(manager.get_permissions(parent))
        return all_perms


class RoleManager:
    """
    Centralized role management for SILA.

    Provides:
    - Role definitions and hierarchy
    - Permission aggregation
    - Role validation
    - Inheritance resolution

    Usage:
        manager = RoleManager()
        manager.register_role("admin", "Administrator", parent_roles={"user"})
        manager.add_permission("admin", "system:*")

        admin_perms = manager.get_permissions("admin")
    """

    def __init__(self):
        """Initialize role manager with built-in system roles"""
        self.roles: dict[str, RoleDefinition] = {}
        self._permission_cache: dict[str, set[str]] = {}

        # Register built-in roles
        self._init_system_roles()

    def _init_system_roles(self) -> None:
        """Initialize built-in system role hierarchy"""
        # Root - absolute power
        self.register_role(
            name=SystemRole.ROOT.value,
            description="Root user with absolute system access",
            permissions={"system:*", "admin:*", "write:*", "read:*"},
        )

        # Super Admin - administrative power
        self.register_role(
            name=SystemRole.SUPER_ADMIN.value,
            description="Super administrator with broad system access",
            parent_roles={SystemRole.ADMIN.value},
            permissions={"admin:*", "user:manage", "audit:view"},
        )

        # Admin - system administration
        self.register_role(
            name=SystemRole.ADMIN.value,
            description="Administrator with system management access",
            parent_roles={SystemRole.MODERATOR.value},
            permissions={"admin:read", "admin:write", "user:moderate"},
        )

        # Moderator - content moderation
        self.register_role(
            name=SystemRole.MODERATOR.value,
            description="Moderator with content review access",
            parent_roles={SystemRole.USER.value},
            permissions={"content:moderate", "user:report"},
        )

        # User - standard user
        self.register_role(
            name=SystemRole.USER.value,
            description="Standard user with basic access",
            parent_roles={SystemRole.GUEST.value},
            permissions={"user:read", "user:write", "content:create"},
        )

        # Guest - minimal access
        self.register_role(
            name=SystemRole.GUEST.value,
            description="Guest user with read-only access",
            permissions={"public:read"},
        )

        # Service accounts
        self.register_role(
            name=SystemRole.SERVICE.value,
            description="Service-to-service authentication role",
            permissions={"service:*"},
        )

        # System role
        self.register_role(
            name=SystemRole.SYSTEM.value,
            description="Internal system role",
            permissions={"system:internal"},
        )

    def register_role(
        self,
        name: str,
        description: str = "",
        parent_roles: set[str] | None = None,
        permissions: set[str] | None = None,
        metadata: dict[str, any] | None = None,
    ) -> None:
        """
        Register a new role in the system.

        Args:
            name: Unique role name
            description: Human-readable role description
            parent_roles: Set of parent roles to inherit from
            permissions: Set of permissions granted to this role
            metadata: Additional metadata (e.g., color, icon for UI)
        """
        # Validate parent roles exist
        if parent_roles:
            for parent in parent_roles:
                if parent not in self.roles:
                    raise ValueError(f"Parent role '{parent}' not registered")

        role = RoleDefinition(
            name=name,
            description=description,
            parent_roles=parent_roles or set(),
            permissions=permissions or set(),
            metadata=metadata or {},
        )

        self.roles[name] = role
        self._permission_cache.clear()

    def add_permission(self, role_name: str, permission: str) -> None:
        """
        Add a permission to a role.

        Args:
            role_name: Name of role
            permission: Permission to add

        Raises:
            ValueError: If role not found
        """
        if role_name not in self.roles:
            raise ValueError(f"Role '{role_name}' not registered")

        self.roles[role_name].permissions.add(permission)
        self._permission_cache.clear()

    def add_permissions_batch(
        self,
        role_name: str,
        permissions: list[str],
    ) -> None:
        """
        Add multiple permissions to a role.

        Args:
            role_name: Name of role
            permissions: List of permissions to add
        """
        if role_name not in self.roles:
            raise ValueError(f"Role '{role_name}' not registered")

        self.roles[role_name].permissions.update(permissions)
        self._permission_cache.clear()

    def get_permissions(self, role_name: str) -> set[str]:
        """
        Get all permissions for a role including inherited permissions.

        Args:
            role_name: Name of role

        Returns:
            Set of all permissions (direct + inherited)

        Raises:
            ValueError: If role not found
        """
        if role_name not in self.roles:
            raise ValueError(f"Role '{role_name}' not registered")

        if role_name in self._permission_cache:
            return self._permission_cache[role_name]

        role = self.roles[role_name]
        all_perms = role.get_all_permissions(self)
        self._permission_cache[role_name] = all_perms

        return all_perms

    def get_role(self, role_name: str) -> RoleDefinition | None:
        """
        Get role definition.

        Args:
            role_name: Name of role

        Returns:
            RoleDefinition or None if not found
        """
        return self.roles.get(role_name)

    def role_exists(self, role_name: str) -> bool:
        """Check if role is registered"""
        return role_name in self.roles

    def get_role_hierarchy(self, role_name: str) -> tuple[list[str], int]:
        """
        Get role hierarchy from root to this role.

        Args:
            role_name: Name of role

        Returns:
            Tuple of (path_to_root, depth)
        """
        if role_name not in self.roles:
            raise ValueError(f"Role '{role_name}' not found")

        visited = set()
        path = [role_name]
        depth = 0

        def traverse(name: str):
            nonlocal depth
            if name in visited:
                return
            visited.add(name)

            if name in self.roles:
                for parent in self.roles[name].parent_roles:
                    path.append(parent)
                    depth += 1
                    traverse(parent)

        traverse(role_name)
        return path, depth

    def has_permission(
        self,
        role_name: str,
        permission: str,
    ) -> bool:
        """
        Check if role has a specific permission.

        Supports wildcard matching (e.g., "admin:*" matches "admin:read").

        Args:
            role_name: Name of role
            permission: Permission to check

        Returns:
            True if role has permission
        """
        if role_name not in self.roles:
            return False

        all_perms = self.get_permissions(role_name)

        # Direct match
        if permission in all_perms:
            return True

        # Wildcard match
        for perm in all_perms:
            if perm.endswith("*"):
                prefix = perm.rstrip("*")
                if permission.startswith(prefix):
                    return True

        return False

    def has_any_permission(
        self,
        role_name: str,
        permissions: list[str],
    ) -> bool:
        """
        Check if role has at least one of the given permissions.

        Args:
            role_name: Name of role
            permissions: List of permissions to check

        Returns:
            True if role has at least one permission
        """
        for permission in permissions:
            if self.has_permission(role_name, permission):
                return True
        return False

    def has_all_permissions(
        self,
        role_name: str,
        permissions: list[str],
    ) -> bool:
        """
        Check if role has all given permissions.

        Args:
            role_name: Name of role
            permissions: List of permissions to check

        Returns:
            True if role has all permissions
        """
        for permission in permissions:
            if not self.has_permission(role_name, permission):
                return False
        return True

    def list_roles(self) -> list[str]:
        """List all registered role names"""
        return list(self.roles.keys())

    def describe_role(self, role_name: str) -> dict[str, any]:
        """
        Get complete role information.

        Args:
            role_name: Name of role

        Returns:
            Dictionary with role details
        """
        if role_name not in self.roles:
            raise ValueError(f"Role '{role_name}' not found")

        role = self.roles[role_name]
        return {
            "name": role.name,
            "description": role.description,
            "parent_roles": list(role.parent_roles),
            "direct_permissions": list(role.permissions),
            "all_permissions": list(self.get_permissions(role_name)),
            "metadata": role.metadata,
        }

    def invalidate_cache(self) -> None:
        """Clear permission cache (use after role changes)"""
        self._permission_cache.clear()
