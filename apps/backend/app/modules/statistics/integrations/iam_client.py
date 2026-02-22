from typing import Optional


class IAMClient:
    @staticmethod
    def get_current_user(token: Optional[str] = None):
        # stub: validate token and return user object
        return {"id": 1, "username": "dev", "permissions": ["statistics:view", "statistics:admin", "statistics:export"]}

    @staticmethod
    def check_permission(user, perm: str) -> bool:
        if not user:
            return False
        return perm in user.get("permissions", [])
