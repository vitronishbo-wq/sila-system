import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


class PermissionCache:
    """Redis-backed permission cache for fast RBAC lookups"""

    def set(self, user_id, roles):
        """Cache user roles with 1-hour TTL"""
        r.set(
            f"perm:{user_id}",
            json.dumps(roles),
            ex=3600
        )

    def get(self, user_id):
        """Retrieve cached permissions"""
        data = r.get(f"perm:{user_id}")
        if not data:
            return None
        return json.loads(data)
