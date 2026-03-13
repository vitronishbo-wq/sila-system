class ZeroTrustEngine:
    """Zero-trust authorization engine - verify every request"""

    def validate(self, user, service, permission):
        """Validate user has permission for service operation"""
        roles = user.get("roles", [])

        # Admin can access everything
        if "admin" in roles:
            return True

        # Check specific permission
        if permission in roles:
            return True

        return False
