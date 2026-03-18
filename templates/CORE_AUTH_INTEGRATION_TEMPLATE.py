"""
CORE AUTH INTEGRATION TEMPLATE
==============================

This file demonstrates how to integrate core/auth components into SILA modules.
Copy this as a starting point for your module's authentication and authorization.

Location: Use this template for any module's routers, endpoints, and services.
"""

# ============================================================================
# EXAMPLE 1: Basic Route Protection with PermissionGuard
# ============================================================================

from fastapi import APIRouter, Depends, HTTPException
from apps.backend.core.auth import (
    JWTHandler,
    PolicyEngine,
    PermissionGuard,
    RoleManager,
)

# Initialize auth components (usually in main.py, but shown here for clarity)
jwt_handler = JWTHandler(secret_key="your-secret-key-here")
policy_engine = PolicyEngine()
permission_guard = PermissionGuard(policy_engine)
role_manager = RoleManager()

# Create router
router = APIRouter(prefix="/documents", tags=["documents"])


# ============================================================================
# PATTERN 1: Require Specific Role
# ============================================================================

@router.get("/admin/all")
async def list_all_documents(
    # This ensures only users with 'admin' role can access this endpoint
    current_user = Depends(permission_guard.require_role("admin")),
) -> dict:
    """
    List all documents (admin only).
    
    The require_role dependency:
    1. Extracts JWT token from Authorization header
    2. Validates token with JWTHandler
    3. Checks user's role with RoleManager
    4. Returns 403 if role not allowed
    """
    return {
        "user_id": current_user.get("sub"),
        "role": current_user.get("role"),
        "documents": ["doc1", "doc2", "doc3"]
    }


# ============================================================================
# PATTERN 2: Custom Permission Check with PolicyEngine
# ============================================================================

@router.post("/documents/{doc_id}/approve")
async def approve_document(
    doc_id: str,
    current_user = Depends(permission_guard.require_authenticated()),
) -> dict:
    """
    Approve a document using PolicyEngine for fine-grained control.
    
    Shows how to:
    - Get current user from FastAPI Depends
    - Use PolicyEngine to check specific resource/action
    - Return custom error messages
    """
    user_role = current_user.get("role", "guest")
    
    # Check if user can approve documents
    decision = policy_engine.authorize(
        user_roles={user_role},
        resource="documents",
        action="approve"
    )
    
    if not decision:
        raise HTTPException(
            status_code=403,
            detail=f"Cannot approve documents: {decision.reason}"
        )
    
    # Process the approval
    return {
        "document_id": doc_id,
        "status": "approved",
        "approved_by": current_user.get("sub"),
    }


# ============================================================================
# PATTERN 3: Multi-role Authorization
# ============================================================================

@router.delete("/documents/{doc_id}")
async def delete_document(
    doc_id: str,
    current_user = Depends(permission_guard.require_authenticated()),
) -> dict:
    """
    Delete a document - requires admin OR document_manager role.
    
    Shows how to:
    - Check multiple roles
    - Use role hierarchy from RoleManager
    """
    user_role = current_user.get("role")
    allowed_roles = {"admin", "document_manager"}
    
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail=f"Role '{user_role}' cannot delete documents. "
                   f"Required: {allowed_roles}"
        )
    
    # Get all permissions for user's role (including inherited)
    permissions = role_manager.get_permissions(user_role)
    
    return {
        "document_id": doc_id,
        "deleted": True,
        "deleted_by": current_user.get("sub"),
        "user_permissions": list(permissions)
    }


# ============================================================================
# PATTERN 4: Resource-based Authorization (Row-level Security)
# ============================================================================

@router.get("/documents/{doc_id}")
async def get_document(
    doc_id: str,
    current_user = Depends(permission_guard.require_authenticated()),
) -> dict:
    """
    Get a document with resource-level authorization.
    
    Shows how to:
    - Check both role AND resource ownership
    - Implement row-level security
    - Use PolicyEngine with resource context
    """
    user_id = current_user.get("sub")
    user_role = current_user.get("role")
    
    # First: Role-level check
    decision = policy_engine.authorize(
        user_roles={user_role},
        resource="documents",
        action="read"
    )
    
    if not decision:
        raise HTTPException(status_code=403, detail="Cannot read documents")
    
    # Second: Resource-level check (example: document ownership)
    # In real implementation, fetch document from DB
    document = {
        "id": doc_id,
        "title": "Sample Document",
        "owner_id": "user-123",  # Would come from DB
    }
    
    # Allow if: owner, admin, or document_reader role
    is_owner = document["owner_id"] == user_id
    is_admin = user_role == "admin"
    is_reader = "read" in role_manager.get_permissions(user_role)
    
    if not (is_owner or is_admin or is_reader):
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this document"
        )
    
    return document


# ============================================================================
# PATTERN 5: Service Layer Authorization
# ============================================================================

class DocumentService:
    """Example service showing auth integration at service layer."""
    
    def __init__(self, policy_engine: PolicyEngine, role_manager: RoleManager):
        self.policy_engine = policy_engine
        self.role_manager = role_manager
    
    def create_document(self, title: str, user_role: str) -> dict:
        """
        Create document with service-layer authorization.
        
        Shows how to:
        - Integrate auth in business logic
        - Reuse PolicyEngine across endpoints
        - Return meaningful errors
        """
        # Check authorization
        decision = self.policy_engine.authorize(
            user_roles={user_role},
            resource="documents",
            action="create"
        )
        
        if not decision:
            raise ValueError(f"Cannot create documents: {decision.reason}")
        
        # Business logic
        return {"id": "doc-456", "title": title, "created": True}


# Dependency to inject service
def get_document_service() -> DocumentService:
    return DocumentService(policy_engine, role_manager)


@router.post("/documents")
async def create_document(
    title: str,
    current_user = Depends(permission_guard.require_authenticated()),
    service: DocumentService = Depends(get_document_service),
) -> dict:
    """Create document using service with built-in authorization."""
    return service.create_document(title, current_user.get("role"))


# ============================================================================
# PATTERN 6: JWT Token Handling
# ============================================================================

from datetime import timedelta


def generate_auth_tokens(user_id: str, role: str) -> dict:
    """
    Generate access and refresh tokens using JWTHandler.
    
    Shows how to:
    - Create tokens with user claims
    - Set custom expiration times
    - Handle token generation for login endpoints
    """
    # Create access token (default: 90 days)
    access_token = jwt_handler.create_access_token(
        subject=user_id,
        additional_claims={"role": role}
    )
    
    # Or with custom expiration
    access_token_short = jwt_handler.create_access_token(
        subject=user_id,
        additional_claims={"role": role},
        expires_delta=timedelta(hours=1)
    )
    
    # Create refresh token
    refresh_token = jwt_handler.create_refresh_token(
        subject=user_id,
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/auth/login")
async def login(username: str, password: str) -> dict:
    """
    Login endpoint that generates JWT tokens.
    
    In real implementation:
    1. Validate username/password
    2. Get user from database
    3. Generate tokens
    """
    # Validate credentials (example only)
    if username == "admin" and password == "admin":
        user_id = "user-admin-123"
        role = "admin"
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return generate_auth_tokens(user_id, role)


@router.post("/auth/refresh")
async def refresh_token(refresh_token: str) -> dict:
    """
    Refresh access token using refresh token.
    
    Shows how to:
    - Validate refresh token
    - Extract claims
    - Issue new access token
    """
    try:
        decoded = jwt_handler.decode_refresh_token(refresh_token)
        user_id = decoded.get("sub")
        
        # In real implementation: fetch user role from database
        role = "user"
        
        new_access_token = jwt_handler.create_access_token(
            subject=user_id,
            additional_claims={"role": role}
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# ============================================================================
# PATTERN 7: Role Hierarchy and Inheritance
# ============================================================================

def setup_role_hierarchy():
    """
    Setup custom role hierarchy for your module.
    
    Shows how to:
    - Define role relationships
    - Set permission inheritance
    - Register custom roles
    
    Call this during application startup.
    """
    # Define role hierarchy:
    # root > admin > moderator > user > guest
    
    role_manager.register_role(
        name="document_admin",
        description="Document administration role",
        parent_roles={"admin"},
        permissions={
            "documents:read",
            "documents:write",
            "documents:delete",
            "documents:approve"
        }
    )
    
    role_manager.register_role(
        name="document_editor",
        description="Can edit documents",
        parent_roles={"user"},
        permissions={
            "documents:read",
            "documents:write"
        }
    )
    
    role_manager.register_role(
        name="document_viewer",
        description="Read-only access",
        parent_roles={"guest"},
        permissions={
            "documents:read"
        }
    )


# ============================================================================
# PATTERN 8: Policy Registration (Module Startup)
# ============================================================================

def register_module_policies():
    """
    Register all policies for documents module.
    
    Shows how to:
    - Define resource/action policies
    - Map roles to permissions
    - Set up batch policy registration
    
    Call this during application startup (in main.py or module init).
    """
    # Individual policy
    policy_engine.register_policy(
        resource="documents",
        action="read",
        required_roles={"user", "admin", "moderator"}
    )
    
    policy_engine.register_policy(
        resource="documents",
        action="write",
        required_roles={"admin", "document_admin", "document_editor"}
    )
    
    policy_engine.register_policy(
        resource="documents",
        action="delete",
        required_roles={"admin", "document_admin"}
    )
    
    # Or batch registration
    policies = [
        {
            "resource": "documents",
            "action": "approve",
            "required_roles": ["admin", "document_admin", "moderator"]
        },
        {
            "resource": "documents",
            "action": "execute_workflow",
            "required_roles": ["admin"]
        },
        {
            "resource": "documents",
            "action": "export",
            "required_roles": ["admin", "document_admin"]
        }
    ]
    
    policy_engine.register_batch(policies)


# ============================================================================
# PATTERN 9: Async Authorization Checks
# ============================================================================

async def check_document_ownership(
    doc_id: str,
    current_user = Depends(permission_guard.require_authenticated()),
) -> dict:
    """
    Dependency for checking document ownership.
    
    Shows how to:
    - Create reusable authorization dependencies
    - Combine FastAPI Depends with auth
    - Use in multiple endpoints
    """
    from datetime import datetime
    
    user_id = current_user.get("sub")
    user_role = current_user.get("role")
    
    # Simulate database lookup
    document = {
        "id": doc_id,
        "owner_id": "user-123",
        "created_at": datetime.now(),
    }
    
    # Role-based fast path
    if user_role == "admin":
        return document
    
    # Owner check
    if document["owner_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't own this document"
        )
    
    return document


@router.put("/documents/{doc_id}")
async def update_document(
    doc_id: str,
    title: str,
    doc: dict = Depends(check_document_ownership),
) -> dict:
    """Update document (owner or admin only)."""
    return {
        "id": doc_id,
        "title": title,
        "updated": True
    }


# ============================================================================
# INITIALIZATION CODE (Put in main.py or module init)
# ============================================================================

def init_auth_for_documents_module():
    """
    Initialize all auth components for documents module.
    
    Call this once during application startup.
    """
    # Setup JWT secret
    jwt_handler.set_secret("your-production-secret-key")
    
    # Setup role hierarchy
    setup_role_hierarchy()
    
    # Register policies
    register_module_policies()
    
    # Verify setup
    print("✓ Documents module auth initialized")
    print(f"  - Roles: {len(role_manager.roles)}")
    print(f"  - Policies: {len(policy_engine.policies)}")


# Exports for this module
__all__ = [
    "router",
    "jwt_handler",
    "policy_engine",
    "permission_guard",
    "role_manager",
    "DocumentService",
    "generate_auth_tokens",
    "setup_role_hierarchy",
    "register_module_policies",
    "init_auth_for_documents_module",
]
