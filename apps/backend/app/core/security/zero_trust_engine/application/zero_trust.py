class ZeroTrustEngine:
    """Zero-trust authorization engine - verify every request"""

    def validate(self, user, service, permission):
        """Validate user has permission for service operation"""
        roles = user.get('roles', [])
        if 'admin' in roles:
            return True
        if permission in roles:
            return True
        return False