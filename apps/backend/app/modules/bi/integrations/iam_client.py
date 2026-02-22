from typing import Optional


class IAMClient:
    @staticmethod
    def get_current_user(token: Optional[str] = None):
        # In real integration, validate token and return user object
        return {"id": 1, "username": "dev", "permissions": ["bi:view", "bi:admin", "bi:export"]}

    @staticmethod
    def check_permission(user, perm: str) -> bool:
        if not user:
            return False
        return perm in user.get("permissions", [])
